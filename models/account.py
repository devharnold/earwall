#!/usr/bin/env python3

"""Account model class"""

import models
import hashlib
import psycopg2
from psycopg2 import sql
import os
import random
from os import getenv
from models import BaseModel
from models.engine.db_storage import get_db_connection
from web3 import HTTPProvider
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify
import paypalrestsdk
from dotenv import load_dotenv
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PORT = os.getenv('DB_PORT')
DB_HOST = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')

class Account(BaseModel):
    """Representation of an account model"""
    def __init__(self, user_id, account_number, balance, password):
        self.user_id = user_id
        self.account_number = account_number
        self.balance = balance
        self.password = password

    @staticmethod
    def generate_account_number():
        """Generate a random digit account number"""
        return ''.join([str(random.randint(0, 9)) for _ in range(13)])
    
    @classmethod
    def create_account(user_id, plain_password: str, username: str, email: str, currency: str, account_type: str, intial_balance: int):
        allowed_currencies = ["GPB", "KES", "USD"]
        available_ccount_types = ["Current, Lock Account, Premium Account"]

        data = request.get_json()
        username = data['username']
        email = data['email']
        plain_password = data['password']
        currency = data['currency']
        account_type = data['account_type']

        if currency not in allowed_currencies:
            return jsonify({"error": "Invalid currencies selected. Allowed currencies are: " + ", ".join(allowed_currencies)}), 400

        hashed_password = generate_password_hash(plain_password)

        # set initial balance to 0
        initial_balance = 0

        try:
            connection = psycopg2.connect(
                dbname=DB_NAME,
                dbport=DB_PORT,
                dbhost=DB_HOST,
                dbpassword=DB_PASSWORD,
            )
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO users (username, email, password, account_type, balance)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (username, email, hashed_password, account_type, intial_balance, currency))

            connection.commit()
            return jsonify({"message": "Account successfully created"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()
        
    def update_account(user_id, stored_hashed_password: str):
        data = request.get_json()
        username = data['username']
        plain_password = data['password']

        def verify_password(input_password: str, hashed_password: str) -> bool:
            if verify_password(input_password: str, stored_hashed_password: str):
            
            return check_password_hash(hashed_password, input_password)

        print("Username:", username)
        print("Input Password:", plain_password)
        print("Stored Password:", stored_hashed_password)

        #if verify_password(input_password: str, stored_hashed_password: str):