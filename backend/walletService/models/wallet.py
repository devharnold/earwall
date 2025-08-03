#!/usr/bin/env python3
"""Implementation of wallet class."""

import psycopg2
from psycopg2 import sql
import os
from backend.userService.models.user import User
from backend.models.baseModel import BaseModel
from flask import jsonify, request
import uuid
from backend.engine.db_storage import DatabaseManager


class Wallet(BaseModel):
    def __init__(self, wallet_id, user_id, balance, currency, password):
        self.wallet_id = str(uuid.uuid4())[:8]
        self.user_id = user_id
        self.password = User.password()
        self.balance = balance
        self.currency = currency

    def create_new_wallet(self, user_id, wallet_id, currency, balance=0.00):
        # create new wallet
        available_currencies = ["GBP", "KES", "USD"]

        if not user_id:
            return jsonify({"error": "Cannot find User"}), 404

        if currency not in available_currencies:
            return jsonify({"error": "Unsupported currency"}), 400

        try:
            # Database operations
            connection = DatabaseManager.get_db_connection()
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO cashwallets (user_id, cashwallet_id, currency, balance)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, wallet_id, currency, balance))
            connection.commit()

            return jsonify({"message": "Wallet created"}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def fetch_wallet_data(self, wallet_id):
        # fetch whole wallet data
        from flask import jsonify

        try:
            # Establish database connection
            connection = DatabaseManager.get_db_connection()
            cursor = connection.cursor()

            # SQL query to fetch wallet data
            cursor.execute("SELECT * FROM wallets WHERE wallet_id = %s", (wallet_id))
            wallet_data = cursor.fetchone()

            if wallet_data:
                # Map data to a readable format
                result = {
                    "user_id": wallet_data[0],
                    "balance": wallet_data[1],
                    "currency": wallet_data[2],
                    "wallet_id": wallet_data[3]
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

    def fetch_wallet_balance(self, wallet_id):
        # Get wallet balance
        try:
            connection = DatabaseManager.get_db_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT balance FROM wallets WHERE wallet_id = %s", (wallet_id))
            wallet_data = cursor.fetchone()

            if wallet_data:
                result = {"balance": wallet_data[0]}
                return jsonify(result), 200
            else:
                return jsonify({"error": "Balance or your wallet isn't found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        finally:
            cursor.close()
            connection.close()