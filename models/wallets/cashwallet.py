#!/usr/bin/env python3
"""Implementation of wallet class."""

import psycopg2
from psycopg2 import sql
import os
from models.account import Account
from models.user import User
from models.baseModel import BaseModel
from flask import jsonify, request
import uuid
from datetime import datetime, timedelta, timezone
from engine.db_storage import get_db_connection


class CashWallet(BaseModel):
    def __init__(self, cashwallet_id, user_id, balance, currency, password):
        self.cashwallet_id = str(uuid.uuid4())[:8]
        self.user_id = user_id
        self.password = User.password()
        self.balance = balance
        self.currency = currency

    @classmethod
    def create_new_wallet(cls, user_id, cashwallet_id, currency, balance=0.00):
        """
        Creates a new wallet for the user.
        """
        available_currencies = ["GBP", "KES", "USD"]

        if not user_id:
            return jsonify({"error": "Cannot find User"}), 404

        if currency not in available_currencies:
            return jsonify({"error": "Unsupported currency"}), 400

        try:
            # Database operations
            connection = get_db_connection()
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO cashwallets (user_id, cashwallet_id, currency, balance)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, cashwallet_id, currency, balance))
            connection.commit()

            return jsonify({"message": "Wallet created"}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    @classmethod
    def fetch_wallet_data(cls, cashwallet_id):
        """Method to fetch cash wallet data for a specific user."""
        from flask import jsonify

        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # SQL query to fetch wallet data
            cursor.execute("SELECT * FROM cashwallets WHERE cashwallet_id = %s", (cashwallet_id))
            wallet_data = cursor.fetchone()

            if wallet_data:
                # Map data to a readable format
                result = {
                    "user_id": wallet_data[0],
                    "balance": wallet_data[1],
                    "currency": wallet_data[2],
                    "cashwallet_id": wallet_data[3]
                }
                return jsonify(result), 200
            else:
                return jsonify({"error": "Cash wallet not found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
