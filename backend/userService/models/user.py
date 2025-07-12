#!/usr/bin/env python3

"""Holds the user model class"""

import hashlib
import os
import uuid
from os import getenv
from backend.models import BaseModel
from backend.email_ms.send_regmail import RegularEmailService
from backend.engine.db_storage import get_db_connection
import paypalrestsdk
import bcrypt

class User:
    """Representation of a user model"""
    def __init__(self, user_id, first_name, last_name, user_email, paypal_id, paypal_email, password):
        self.user_id = str(uuid.uuid4())[:8]
        self.first_name = first_name
        self.last_name = last_name
        self.email = user_email
        self.password = password
        self.paypal_id = paypal_id
        self.paypal_email = paypal_email

    def create_user(self, first_name, last_name, user_email, password, user_id):
        """Function to create a user and insert into the database."""
        from flask import jsonify

        # Hash the password
        hashed_password = self.hash_password(password)

        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Begin transaction
            connection.autocommit = False

            # SQL query to insert the user
            insert_query = """
            INSERT INTO users (user_id, first_name, last_name, user_email, password)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, first_name, last_name, user_email, hashed_password))

            # Commit transaction
            connection.commit()

            RegularEmailService.send_welcome_mail()

            return jsonify({"message": "User created successfully"}), 201

        except Exception as e:
            # Rollback in case of an error
            connection.rollback()
            return jsonify({"error": str(e)}), 500

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def hash_password(self, password):
        """Hash a user's password using the sha256 algorithm and add salt"""
        salt = os.urandom(16) # New salt
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 16)
        return salt, hashed_password
    
    def find_user_by_email(email):
        connection  = get_db_connection()
        with connection.cursor() as cursor:
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, email())
            result = cursor.fetchone()
            if result:
                return {
                    "first_name": result['first_name'],
                    "last_name": result['last_name'],
                    "email": result['email'],
                    "wallet_id": result['wallet_id']
                }
            return None
        
    def find_user_by_id(user_id):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(query, user_id())
            result = cursor.fetchone()
            if result:
                return {
                    "first_name": result['first_name'],
                    "last_name": result['last_name'],
                    "email": result['email'],
                    "wallet_id": result['wallet_id']
                }
            return None
            
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def save(self):
        """Saves a new user to the db"""
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO users (first_name, last_name, user_email, user_id, password)
        VALUES (%s, %s, %s, %s, %s);
        """
        try:
            cursor.execute(query, (self.first_name, self.last_name, self.user_email, self.hashed_password))
            connection.commit()
            print("User saved successfully")
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_password(user_email, new_password):
        """Updates the password of an existing user."""
        connection = get_db_connection()
        cursor = connection.cursor()

        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        query = "UPDATE users SET password = %s WHERE user_email = %s;"
        try:
            cursor.execute(query, (hashed_password, user_email))
            connection.commit()
            print("Password saved successfully")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

class ValidatePaypalId:
    """Class that handles user paypal id"""
    class PaypalConfig:
        """handles paypal sdk configuration"""
        def __init__(self, client_id: str, client_secret: str, mode: str = "sandbox"):
            paypalrestsdk.configure({
                "mode": mode,
                "client_id": client_id,
                "client_secret": client_secret
            })

    def __init__(self, client_id: str, client_secret: str, mode: str = "sandbox"):
        """Initialize paypal configuration"""
        self.config = self.PaypalConfig(client_id, client_secret, mode)