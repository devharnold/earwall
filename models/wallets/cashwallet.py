#!/usr/bin/env python3
"""Implementation of wallet class."""

import psycopg2
from psycopg2 import sql
import os
from models.account import Account
from models.baseModel import BaseModel
from models.user import User
from flask import jsonify, request
import uuid
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash
from engine.db_storage import get_db_connection


class CashWallet(BaseModel):
    def __init__(self, cashwallet_id, user_id, balance, currency, password):
        self.cashwallet_id = str(uuid.uuid4())[:8]
        self.user_id = user_id
        self.password = password
        self.balance = balance
        self.currency = currency

    @classmethod
    def create_new_wallet(cls, username: str, password: str, user_id: int, cashwallet_id: int, currency: str, balance: int):
        available_currencies = ["GBP", "KES", "USD"]
        wallet_types = ["Premium", "Regular"]

        data = request.get_json()
        username = data['username']
        user_id = data['user_id']
        cashwallet_id = data['cashwallet_id']
        currency = data['currency']
        wallet_type = data['wallet_type', 'Regular'] #default to regular
        
        if not user_id:
            return jsonify({"error": "Cannot find User"}), 404
        
        if currency not in available_currencies:
            return jsonify({"error": "Unsupported currency"}), 400
        
        if wallet_type not in wallet_types:
            return jsonify({"error": "Invalid wallet type"}), 400

        hashed_password =generate_password_hash(password)
        
        try:
            conn=get_db_connection()
            cursor=conn.cursor()

            insert_query = """
            INSERT INTO cash_wallet (user_id, password, username, wallet_id, balance)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, password, username, cashwallet_id, balance))
            conn.commit()
            return jsonify({"message": "Wallet created"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()