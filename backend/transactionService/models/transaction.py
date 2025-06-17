#!/usr/bin/env python3

"""Transaction model class"""

import psycopg2
from psycopg2 import sql
from models.baseModel import BaseModel
from backend.models.wallet import Wallet
from backend.email_ms.send_transmail import EmailTransactionService
import os
from flask import jsonify
import random
import string
import requests
from decimal import Decimal
from backend.engine.db_storage import get_db_connection
from dotenv import load_dotenv
load_dotenv()


class Transaction:
    """Transaction model"""
    def __init__(self, sender_email, receiver_email, amount, from_currency, to_currency, transaction_id):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.amount = Decimal(amount)
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.transaction_id = self.generate_transaction_id()

    def process_p2p_transaction(cls, transactions):
        """Initiates a transaction between two users in a P2P EFT service with currency conversion."""
        available_currencies = {"GBP", "USD", "KES"}

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            connection.autocommit = False  # Explicitly start transaction

            result = []

            for transaction in transactions:
                sender_email = transaction['sender_email']
                receiver_email = transaction['receiver_email']
                from_currency = transaction['from_currency']
                to_currency = transaction['to_currency']
                amount = transaction['amount']
                transaction_id = transaction['transaction_id']

                # Validate amount
                if amount <= 0:
                    result.append({"transaction_id": transaction_id, "status": "Incomplete! Cannot transfer 0 funds"})
                    continue

                # Validate currencies
                if from_currency not in available_currencies or to_currency not in available_currencies:
                    result.append({"transaction_id": transaction_id, "status": "Currency not available!"})
                    continue

                # Check sender's balance
                cursor.execute("SELECT balance FROM wallets WHERE cashwallet_id = %s", (sender_email,))
                sender_data = cursor.fetchone()
                if not sender_data:
                    result.append({"transaction_id": transaction_id, "status": "Sender wallet not found"})
                    continue

                sender_balance = sender_data[0]
                if sender_balance < amount:
                    result.append({"transaction_id": transaction_id, "status": "Insufficient funds in your wallet"})
                    continue

                # Check receiver's wallet
                cursor.execute("SELECT balance FROM wallets WHERE wallet_id = %s", (receiver_email,))
                receiver_data = cursor.fetchone()
                if not receiver_data:
                    result.append({"transaction_id": transaction_id, "status": "Receiver wallet not found!"})
                    continue

                # Deduct from sender
                cursor.execute(
                    "UPDATE wallets SET balance = balance - %s WHERE wallet_id = %s",
                    (amount, sender_email)
                )
                EmailTransactionService.send_sent_funds()

                # Add to receiver
                cursor.execute(
                    "UPDATE wallets SET balance = balance + %s WHERE wallet_id = %s",
                    (amount, receiver_email)
                )
                EmailTransactionService.send_received_funds()

                # Log transaction
                cursor.execute(
                    """
                    INSERT INTO transactions (sender_email, receiver_email, from_currency, to_currency, amount, transaction_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (sender_email, receiver_email, from_currency, to_currency, amount, transaction_id)
                )

                result.append({"transaction_id": transaction_id, "status": "Transaction Complete"})

            # Commit transaction
            connection.commit()
            return result

        except Exception as e:
            connection.rollback()
            return jsonify({"error": "Transaction failed", "message": str(e)}), 500

        finally:
            cursor.close()
            connection.close()

    
    def process_batch_transactions(b_transactions):
        available_currencies = ["GBP", "USD", "KES"]

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            connection.autocommit = False

            results = []

            for b_transaction in b_transactions:
                sender_email = b_transaction['sender_email']
                receivers = b_transaction['receivers']
                from_currency = b_transaction['from_currency']
                to_currency = b_transaction['to_currency']
                amount = b_transaction['amount']
                transaction_id = b_transaction['transaction_id']

                while sender_email:
                    if amount <= 0:
                        results.append({"transaction_id": transaction_id, "status": " Failed. Insufficient funds"})
                        continue

                    if from_currency not in available_currencies and to_currency not in available_currencies:
                        results.append({"transaction_id": transaction_id, "status": "Failed. Currency not available."})
                        continue

                cursor.execute("SELECT balance FROM wallets WHERE wallet_id = %s", (sender_email,))
                sender_data = cursor.fetchone()
                if not sender_data:
                    results.append({"transaction_id": transaction_id, "status": "Sender wallet not found"})
                    continue

                sender_balance = sender_data[0]
                if sender_balance < amount:
                    results.append({"transaction_id": transaction_id, "status": "Insufficient funds in your wallet"})
                    continue

                for receiver in receivers:
                    receiver_email = receiver['receiver_email']
                    receiver_amount = receiver['amount']
                    receiver_transaction_id = receiver['transaction_id']

                    cursor.execute(
                        """
                        INSERT INTO transactions (sender_email, receiver_email, amount, from_currency, to_currency, transaction_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (sender_email, receiver_email, from_currency, to_currency, amount, transaction_id)
                    )
                    sender_balance -= receiver_amount # Deduct the balance from sender's wallet to the receivers' wallets
                    results.append({"transaction_id": receiver_transaction_id, "status": "Transaction Complete"})
            
            connection.commit()
            return results
        except Exception as e:
            connection.rollback()
            return {"error": "Batch process failed", "message": str(e)}, 500
        finally:
            connection.close()
            cursor.close()


    def fetch_transaction_data(sender_email, receiver_email, from_currency, to_currency, amount, transaction_id):
        """Fetch P2P transactions that have been done by a specific user"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            connection.autocommit = False

            result = []
            for transaction in transaction:
                sender_email = transaction['sender_email']
                receiver_email = transaction['receiver_email']
                from_currency = transaction['from_currency']
                to_currency = transaction['to_currency']
                amount = transaction['amount']
                transaction_id = transaction['transaction_id']

                cursor.execute("SELECT * FROM transactions")
                transaction_data = cursor.fetchall()
                if not transaction_data:
                    result.append({"status": "No transactions found"})
                    continue
                
                connection.commit()
                return result
        except Exception as e:
            connection.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            connection.close()
            cursor.close()

    @classmethod
    def generate_transaction_id(cls):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=10))


    @staticmethod
    def convert_currency(cls, amount: Decimal, from_currency: str, to_currency: str) -> Decimal:
        """Converts an amount from one currency to another"""
        if from_currency == to_currency:
            return amount

        exchange_rate = cls.get_exchange_rate(from_currency, to_currency)
        return amount * Decimal(exchange_rate)

    @classmethod
    def get_exchange_rate(cls, from_currency: str, to_currency: str) -> float:
        """Fetches exchange rate between two currencies."""
        """This exchange rate function only works for internal transactions: transactions within the app."""
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and "rates" in data:
            exchange_rate = data['rates'].get(to_currency)
            if exchange_rate:
                return exchange_rate
            else:
                raise ValueError(f"Exchange rate not available for {to_currency}")
        else:
            raise ValueError("Failed to fetch exchange rates")
