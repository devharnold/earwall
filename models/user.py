#!/usr/bin/env python3

"""Holds the user model class"""

import paypalrestsdk.config
import models
import hashlib
import psycopg2
import os
import uuid
from os import getenv
from models import BaseModel
from email_ms.send_regmail import RegularEmailService
from engine.db_storage import get_db_connection
from kafka import KafkaConsumer
import paypalrestsdk
import logging
import json
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
    
    @classmethod
    def find_user_by_email(cls, email):
        connection = get_db_connection()
        with connection:
            with connection.cursor() as cursor:
                query = "SELECT * FROM users WHERE email = %s"
                cursor.execute(query, (email))
                result = cursor.fetchone()
                if result:
                    return cls(
                        first_name=result['first_name'],
                        last_name=result['last_name'],
                        user_email=result['user_email']
                    )
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

    #def verify_paypal_id(self, paypal_email: str, amount: str = "0.01", currency: str = "USD") -> bool:
    #    """Verify if the given paypal email is valid by trying to send a small test payment
    #    params:
    #        paypal_email: user's paypal email
    #        amount: The amount to use for validation, default is ("0.01")
    #        currency: The currency to use for the payment, default is ("USD")
    #        return: True if email is valid, false otherwise
    #    """
    #    try:
    #        payment = payment({
    #            "intent": "sale",
    #            "payer": {
    #                "payment_method": "paypal"
    #            },
    #            "transactions": [{
    #                "amount": {
    #                    "total": amount,
    #                    "currency": currency
    #                },
    #                "payee": {
    #                    "email": paypal_email
    #                },
    #                "description": "Paypal email verification"
    #            }],
    #            "redirect_urls": {
    #                "return_url": "http://localhost:3000/payment/success",
    #                "cancel_url": "http://localhost:3000/payment/cancel"
    #            }
    #        })
    #        
    #        if payment.create():
    #            logging.info("Payment created successfully")
    #            return True
    #        else:
    #            logging.error(f"Payment failed: {payment.error}")
    #            return False
    #        
    #    except Exception as e:
    #        logging.error(f"Error verifying paypalID: {e}")
    #        return False
        
    #def consume_notifications():
    #    """Kafka consumer function to consume paypal config notifications"""
    #    consumer = KafkaConsumer(
    #        'deactivation-notifications',
    #        bootstrap_servers = ['localhost:9092'],
    #        value_desirializer=lambda m: json.loads(m.decode('utf-8'))
    #    )
    #    for message in consumer:
    #        user_email = message.value.get("user_email")
    #        created_wallet = message.value.get("expiration_days")