"""Implementation of wallet class."""

import psycopg2
from psycopg2 import sql
import os
from models.account import Account
from models.baseModel import BaseModel
from models.user import User
from flask import jsonify, request
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash
from kafka import KafkaProducer, KafkaConsumer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from dotenv import load_dotenv
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PORT = os.getenv('DB_PORT')


class CashWallet:
    def __init__(self, wallet_id, user_id, username, user_email, balance, currency, password):
        self.wallet_id = wallet_id
        self.user_id = user_id
        self.password = password
        self.balance = balance
        self.currency = currency
        self.username = username
        self.user_email = user_email
    
    kafka_topic = 'deactivation_notifications'
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'], #This is the Kafka broker address
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    @classmethod
    def create_new_wallet(cls, username: str, password: str, user_id: int, wallet_id: int, currency: str, balance: int):
        available_currencies = ["GBP", "KES", "USD"]
        wallet_types = ["Premium", "Regular"]

        data = request.get_json()
        username = data['username']
        user_id = data['user_id']
        wallet_id = data['wallet_id']
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
            connection = psycopg2.connect(
                name=DB_NAME,
                user=DB_USER,
                port=DB_PORT,
                host=DB_HOST,
                password=DB_PASSWORD
            )
            cursor = connection.cursor()

            #connection.autocommit

            insert_query = """
            INSERT INTO cash_wallet (user_id, password, username, wallet_id, balance)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, password, username, wallet_id, balance))
            connection.commit()
            return jsonify({"message": "Wallet created"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def delete_wallet(cls, user_id: int, wallet_id: int, balance: int):
        try:
            connection = psycopg2.connect(
                name=DB_NAME,
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cursor = connection.cursor()

            connection.autocommit = False

            cursor.execute("SELECT balance FROM cash_wallet WHERE wallet_id = %s", (wallet_id))
            result = cursor.fetchone()

            if not result:
                return jsonify({"error": "Wallet not found"}), 404
            
            balance, wallet_type = result
            #if wallet_type != "Premium":
            #    return jsonify({"error": "Only premium wallets can be deleted"}), 403
            
            if balance > 0 or balance < 0:
                return jsonify({"error": "Cannot delete a wallet with a non-zero balance"})

            cursor.execute("DELETE FROM spend_history WHERE wallet_id = %s", (wallet_id))

            cursor.execute("DELETE FROM cash_wallet WHERE wallet_id = %s", (wallet_id))
            connection.commit()

            return jsonify({"message": "Premium wallet successfully deleted!"}), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()

    def send_email_notification(user_email, expiration_days):
        """Sends an email to the user to alert the user
        who deactivated a wallet to check on the expiration days
        """
        sender_email = "your_email@example.com"
        sender_password = "your_email_password"
        subject = "Your wallet has been deactivated!"
        body = f"""
        Dear User,
        
        Your wallet has been successfully deactivated! It will be permanently deleted after {expiration_days} unless reactivated.
        
        Thank you,
        H arnold & nerd Service Team.
        """

        msg = MIMEMultipart()
        msg["FROM"] = sender_email
        msg["TO"] = user_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP("smtp.example.com", 587)as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, user_email, msg.as_string())
            print("Deactivation email successfully sent")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def consume_notifications():
        """Kafka activities happening over here"""
        consumer = KafkaConsumer(
            'deactivation-notifications',
            bootstrap_servers=['localhost:9092'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

        for message in consumer:
            user_email = message.value.get("user_email")
            expiration_days = message.value.get("expiration_days")

            #send the email notification
            send_email_notification(user_email, expiration_days)