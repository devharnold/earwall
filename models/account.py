#!/usr/bin/env python3

"""Account model class"""

import models
import psycopg2
from psycopg2 import sql
import os
import random
from datetime import datetime
from os import getenv
from models.user import User
from models import BaseModel
from engine.db_storage import get_db_connection
from flask import request, jsonify


class Account(BaseModel):
    """Representation of an account model"""
    def __init__(self, user_id, account_id, balance, currency, password):
        self.user_id = user_id
        self.account_number = account_id
        self.balance = balance
        self.currency = currency
        self.password = User.password()

    @staticmethod
    def generate_account_number():
        """Generate a random digit account number"""
        return ''.join([str(random.randint(0, 9)) for _ in range(13)])
    
    @classmethod
    def create_account(user_id, account_id, currency, balance):
        available_currencies = ["GPB", "KES", "USD"]
        #available_ccount_types = ["Current, Lock Account, Premium Account"]

        data = request.get_json()
        user_id = data['user_id']
        account_id = data['account_id']
        currency = data['currency']
        balance = data['balance']

        if currency not in available_currencies:
            return jsonify({"error": "Invalid currencies selected. Allowed currencies are: " + ", ".join(available_currencies)}), 400


        # set initial balance to 0
        initial_balance = 0.00

        try:
            connection = get_db_connection()
            cursor=connection.cursor()

            insert_query = """
            INSERT INTO user_accounts (user_id, account_id, password, account_type, balance)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, account_id, currency, balance))

            connection.commit()
            return jsonify({"message": "Account successfully created"}), 201
        except Exception as e:
            connection.rollback() #after an unsuccessful connection attempt
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def fetch_account_data(cls, account_id):
        """Method to fetch a user's account details/data"""
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM user_accounts WHERE account_id = %s", (account_id))
            account_data = cursor.fetchone()

            if account_data:
                result = {
                    "user_id": account_data[0],
                    "account_id": account_data[1],
                    "currency": account_data[2],
                    "balance": account_data[3]
                }
                return jsonify(result), 200
            else:
                return jsonify({"error": "Account data not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()