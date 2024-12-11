#!/usr/bin/env python3

"""Transaction model class"""

import psycopg2
from psycopg2 import sql
from models.baseModel import BaseModel
import os
from flask import jsonify
import uuid
import requests
from decimal import Decimal
from engine.db_storage import get_db_connection
from dotenv import load_dotenv

load_dotenv()

class Transaction(BaseModel):
    """Transaction model"""

    def __init__(self, sender_user_id, receiver_user_id, amount, from_currency, to_currency):
        self.sender_user_id = sender_user_id
        self.receiver_user_id = receiver_user_id
        self.amount = Decimal(amount)
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.transaction_id = str(uuid.uuid4())

    @classmethod
    def process_p2p_transaction(cls, sender_user_id, receiver_user_id, amount, sender_cashwallet_id, receiver_cashwallet_id, from_currency, to_currency):
        """Initiates a transaction between two users in a P2P EFT service with currency conversion."""
        available_currencies = ["GBP", "USD", "KES"]
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            if amount <= 0:
                return jsonify({"error": "You cannot transact 0 funds"}), 400

            if from_currency not in available_currencies or to_currency not in available_currencies:
                return jsonify({"error": "Currency not available"}), 400

            conn.autocommit = False

            # Fetch sender wallet balance
            cursor.execute("SELECT balance, currency FROM cashwallets WHERE cashwallet_id = %s", (sender_cashwallet_id,))
            sender_data = cursor.fetchone()
            if not sender_data:
                return jsonify({"error": "Sender wallet not found."}), 404

            sender_balance, from_currency_db = sender_data
            sender_balance = Decimal(sender_balance)

            if sender_balance < amount:
                return jsonify({"error": "Insufficient funds in your wallet!"}), 400

            if from_currency != from_currency_db:
                return jsonify({"error": "Sender currency mismatch!"}), 400

            # Convert currency if needed
            if from_currency != to_currency:
                amount = cls.convert_currency(amount, from_currency, to_currency)

            # Update balances
            cursor.execute("UPDATE cashwallets SET balance = balance - %s WHERE cashwallet_id = %s", (amount, sender_cashwallet_id))
            cursor.execute("UPDATE cashwallets SET balance = balance + %s WHERE cashwallet_id = %s", (amount, receiver_cashwallet_id))

            # Log the transaction
            cursor.execute(
                """
                INSERT INTO transactions (sender_user_id, receiver_user_id, sender_cashwallet_id, receiver_cashwallet_id, amount, transaction_type, transaction_id, from_currency, to_currency)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING transaction_id
                """,
                (sender_user_id, receiver_user_id, sender_cashwallet_id, receiver_cashwallet_id, amount, 'P2P Transfer', uuid.uuid4(), from_currency, to_currency)
            )
            transaction_id = cursor.fetchone()[0]
            conn.commit()

            return jsonify({"message": "Transaction completed successfully", "transaction_id": transaction_id}), 201

        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def convert_currency(cls, amount: Decimal, from_currency: str, to_currency: str) -> Decimal:
        """Converts an amount from one currency to another"""
        if from_currency == to_currency:
            return amount

        exchange_rate = cls.get_exchange_rate(from_currency, to_currency)
        return amount * Decimal(exchange_rate)

    @classmethod
    def get_exchange_rate(cls, from_currency: str, to_currency: str) -> float:
        """Fetches exchange rate between two currencies."""
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
    def withdraw_from_account(cls, account_id, amount, cashwallet_id):
        """Withdraw funds from an account to a wallet."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            conn.autocommit = False

            # Check account balance
            cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
            account_balance = cursor.fetchone()
            if not account_balance or Decimal(account_balance[0]) < amount:
                return jsonify({"error": "Insufficient funds in account!"}), 400

            # Update account and wallet balances
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, account_id))
            cursor.execute("UPDATE cashwallets SET balance = balance + %s WHERE cashwallet_id = %s", (amount, cashwallet_id))

            # Log the transaction
            cursor.execute(
                """
                INSERT INTO transactions (account_id, cashwallet_id, amount, transaction_type, status)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (account_id, cashwallet_id, amount, 'Withdrawal', 'Completed')
            )

            conn.commit()
            return jsonify({"message": "Withdrawal successful"}), 201

        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def deposit_to_account(cls, amount, account_id, cashwallet_id):
        """Deposit funds from a wallet to an account."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            conn.autocommit = False

            # Check wallet balance
            cursor.execute("SELECT balance FROM cashwallets WHERE cashwallet_id = %s", (cashwallet_id,))
            wallet_balance = cursor.fetchone()
            if not wallet_balance or Decimal(wallet_balance[0]) < amount:
                return jsonify({"error": "Insufficient funds in wallet!"}), 400

            # Update wallet and account balances
            cursor.execute("UPDATE cashwallets SET balance = balance - %s WHERE cashwallet_id = %s", (amount, cashwallet_id))
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, account_id))

            # Log the transaction
            cursor.execute(
                """
                INSERT INTO transactions (cashwallet_id, account_id, amount, transaction_type, status)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (cashwallet_id, account_id, amount, 'Deposit', 'Completed')
            )

            conn.commit()
            return jsonify({"message": "Deposit successful"}), 201

        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()
