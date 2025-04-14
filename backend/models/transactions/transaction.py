#!/usr/bin/env python3

"""Transaction model class"""

import psycopg2
from psycopg2 import sql
from models.baseModel import BaseModel
from backend.models.wallets.cashwallet import CashWallet
from backend.email_ms.send_transmail import EmailTransactionService
import os
from flask import jsonify
import random
import string
import asyncio
import uuid
import requests
from decimal import Decimal
from backend.engine.db_storage import get_db_connection
from dotenv import load_dotenv
load_dotenv()


class Transaction:
    """Transaction model"""
    def __init__(self, sender_user_id, receiver_user_id, amount, from_currency, to_currency, transaction_id):
        self.sender_user_id = sender_user_id
        self.receiver_user_id = receiver_user_id
        self.amount = Decimal(amount)
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.transaction_id = self.generate_transaction_id()

    @classmethod
    def process_p2p_transaction(cls, transactions):
        """Initiates a transaction between two users in a P2P EFT service with currency conversion."""
        available_currencies = {"GBP", "USD", "KES"}

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            connection.autocommit = False  # Explicitly start transaction

            result = []

            for transaction in transactions:
                sender_user_id = transaction['sender_user_id']
                receiver_user_id = transaction['receiver_user_id']
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
                cursor.execute("SELECT balance FROM cashwallets WHERE cashwallet_id = %s", (sender_user_id,))
                sender_data = cursor.fetchone()
                if not sender_data:
                    result.append({"transaction_id": transaction_id, "status": "Sender wallet not found"})
                    continue

                sender_balance = sender_data[0]
                if sender_balance < amount:
                    result.append({"transaction_id": transaction_id, "status": "Insufficient funds in your wallet"})
                    continue

                # Check receiver's wallet
                cursor.execute("SELECT balance FROM cashwallets WHERE cashwallet_id = %s", (receiver_user_id,))
                receiver_data = cursor.fetchone()
                if not receiver_data:
                    result.append({"transaction_id": transaction_id, "status": "Receiver wallet not found!"})
                    continue

                # Deduct from sender
                cursor.execute(
                    "UPDATE cashwallets SET balance = balance - %s WHERE cashwallet_id = %s",
                    (amount, sender_user_id)
                )

                # Add to receiver
                cursor.execute(
                    "UPDATE cashwallets SET balance = balance + %s WHERE cashwallet_id = %s",
                    (amount, receiver_user_id)
                )

                # Log transaction
                cursor.execute(
                    """
                    INSERT INTO transactions (sender_user_id, receiver_user_id, from_currency, to_currency, amount, transaction_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (sender_user_id, receiver_user_id, from_currency, to_currency, amount, transaction_id)
                )

                # Send email notifications
                EmailTransactionService.send_sent_funds()
                EmailTransactionService.send_received_funds()

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


    @classmethod
    def fetch_transaction_data(cls, sender_user_id, receiver_user_id, from_currency, to_currency, amount, transaction_id):
        """Fetch P2P transactions that have been done by a specific user"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            connection.autocommit = False

            result = []
            for transaction in transaction:
                sender_user_id = transaction['sender_user_id']
                receiver_user_id = transaction['receiver_user_id']
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

    
    def generate_transaction_id():
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

    @classmethod
    def withdraw_from_account(cls, user_account_id, amount, cashwallet_id):
        """Withdraw funds from an account to a wallet."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            connection.autocommit = False

            # Fetch the account url endpoint and check the balance, if the balance is less than amount
            # therefore reject the transaction. Do not bypass

            # Update account and wallet balances
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE user_account_id = %s", (amount, user_account_id))
            cursor.execute("UPDATE cashwallets SET balance = balance + %s WHERE cashwallet_id = %s", (amount, cashwallet_id))

            # Log the transaction
            cursor.execute(
                """
                INSERT INTO transactions (user_account_id, cashwallet_id, amount, transaction_type, status)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (user_account_id, cashwallet_id, amount, 'Withdrawal',)
            )

            connection.commit()
            return jsonify({"message": "Withdrawal successful"}), 201

        except Exception as e:
            connection.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def deposit_to_account(cls, amount, user_account_id, cashwallet_id):
        """Deposit funds from a wallet to an account."""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            connection.autocommit = False

            # supposed to add a url endpoint to connect with the accounts in payments service

            # Check wallet balance
            cursor.execute("SELECT balance FROM cashwallets WHERE cashwallet_id = %s", (cashwallet_id,))
            wallet_balance = cursor.fetchone()
            if not wallet_balance or Decimal(wallet_balance[0]) < amount:
                return jsonify({"error": "Insufficient funds in wallet!"}), 400

            # Update wallet and account balances
            cursor.execute("UPDATE cashwallets SET balance = balance - %s WHERE cashwallet_id = %s", (amount, cashwallet_id))
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, user_account_id))

            # Log the transaction
            cursor.execute(
                """
                INSERT INTO transactions (cashwallet_id, account_id, amount, transaction_type, status)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (cashwallet_id, user_account_id, amount, 'Deposit',)
            )

            connection.commit()
            return jsonify({"message": "Deposit successful"}), 201

        except Exception as e:
            connection.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()
