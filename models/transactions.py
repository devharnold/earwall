#!/usr/bin/env python3

"""Transaction model class"""

import psycopg2
from psycopg2 import sql
from models.wallets import CashWallet
import os
from flask import jsonify, request
from engine.kafka_producer import KafkaProducerInstance
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from dotenv import load_dotenv
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PORT = os.getenv('DB_PORT')
DB_HOST = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')

kafka_instance = KafkaProducerInstance()

class Transaction(CashWallet):
    """Transaction model"""
    def __init__(self, user_email: str, sender_wallet, receiver_wallet, amount: float, transaction_type: str, transaction_id: str):
        self.user_email = user_email
        self.sender_wallet = sender_wallet
        self.receiver_wallet = receiver_wallet
        self.amount = amount
        self.transaction_type = transaction_type
        self.transaction_id = transaction_id

    #kafka_topics = 'transaction_notifications'
    #producer = KafkaProducer(
    #    bootstrap_servers=['localhost:9092'],
    #    value_serializer=lambda v: json.dumps(v).encode('utf-8')
    #)

    @classmethod
    def process_p2p_transaction(cls, user_email: str, sender_wallet_id, receiver_wallet_id, amount, transaction_id: str):
        """Initiates a transaction to take place between different accounts, an p2p eft service."""
        try:
            connection = psycopg2.connect(
                name=DB_NAME,
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cursor = connection.cursor()

            if amount <= 0:
                return jsonify({"error": "You cannot transact 0 funds" }), 400
            
            # Prevents from performing an auto-commit
            connection.autocommit = False

            cursor.execute("SELECT balance FROM users WHERE wallet_id = %s", (sender_wallet_id,))
            sender_balance = cursor.fetchone()
            if sender_balance is None:
                return jsonify({"error": "Sender wallet not found."}), 404
            sender_balance = sender_balance[0]

            if sender_balance < amount:
                return jsonify(({"error": "Insufficient funds in your wallet!"})), 400
            
            cursor.execute("UPDATE users SET balance = balance - %s WHERE wallet_id = %s", (amount, sender_wallet_id))
            cursor.execute("UPDATE users SET balance = balance + %s WHERE wallet_id = %s", (amount, receiver_wallet_id))

            #Log the transaction
            cursor.execute(
                """
                INSERT INTO transactions (user_email, sender_wallet_id, receiver_wallet_id, amount, transaction_id)
                VALUES (%s, %s, %s, %s, %s) RETURNING id
                """,
                (user_email, sender_wallet_id, receiver_wallet_id, amount, transaction_id)
            )
            transaction_id = cursor.fetchone()[0]
            connection.commit()

            # notify via kafka
            cls.send_kafka_p2p_transfer_update(user_email, sender_wallet_id, receiver_wallet_id, amount, transaction_id)

            # Return a message
            return jsonify({"message": "Transaction Completed successfully", "transaction_id": transaction_id}), 201
        
        except Exception as e:
            connection.rollback() # After an unsuccessful connection
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def send_p2p_transfer_update(user_email, sender_wallet, receiver_wallet, amount, transaction_id):
        """Sends an update to the Kafka topic for every p2p transaction"""
        transaction_data = {
            "user_email": user_email,
            "sender_wallet": sender_wallet,
            "receiver_wallet": receiver_wallet,
            "amount": amount,
            "transaction_id": transaction_id
        }
        kafka_instance.send_p2p_transfer_update(transaction_data)

    @classmethod
    def withdraw_from_account(cls, account_id, balance: float, wallet_id, amount, transaction_id):
        try:
            connection = psycopg2.connect(
                name = DB_NAME,
                port = DB_PORT,
                host = DB_HOST,
                password = DB_PASSWORD,
                user = DB_USER 
            )
            cursor = connection.cursor()

        # Perform the balance check on the user's account.
            if balance < amount:
                return jsonify({"error": "You cant withdraw. You don't have funds!"}), 400

            connection.autocommit = False

            # Perform a balance check from the user's account
            cursor.execute("SELECT balance FROM users WHERE account_number = %s", (account_id))
            account_balance = cursor.fetchone()
            if not account_balance:
                raise ValueError("Account does not exist!!!")
            
            if account_balance < amount:
                raise ValueError("Insufficient funds. Cannot perform action!")
            
            if not wallet_id:
                raise ValueError("Wallet not found!")
            
            # Subtract funds from the account to the wallet
            cursor.execute(
                "UPDATE users SET account_balance = balance -%s WHERE account_number = %s", (account_id, amount)
            )
            
            # Add funds to the wallet
            cursor.execute(
                "UPDATE users SET wallet_balance = balance + %s WHERE wallet_id = %s", (wallet_id, amount)
            )

            # Log that transaction activity
            cursor.execute(
                """
                INSERT INTO transactions (account_id, wallet_id, amount, transaction_type, status)
                VALUES (%s, %s, %s, %s, %s)
                """, (account_id, wallet_id, amount, transaction_type, 'Completed')
            )
            connection.commit()
            print("Withdrawal successful.")
            cls.send_kafka_withdraw_transfer_update(account_id, wallet_id, amount, transaction_id)


        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            print("Transaction failed. Error!:", error)

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def send_withdraw_from_account_update(user_email, account_id, wallet_id, amount, transaction_id):
        """Sends an update to the Kafka topic for every p2p transaction"""
        transaction_data = {
            "user_email": user_email,
            "account_id": account_id,
            "wallet_id": wallet_id,
            "amount": amount,
            "transaction_id": transaction_id
        }
        kafka_instance.send_withdraw_from_account_update(transaction_data)


    @classmethod
    def deposit_to_account(cls, amount, account_id, wallet_id, transaction_id):
        """deposit funds from the wallet to your account."""
        try:
            connection = psycopg2.connect(
                name= DB_NAME,
                user=DB_USER,
                port=DB_PORT,
                host=DB_HOST,
                password=DB_PASSWORD
            )
            cursor = connection.cursor()

            if wallet_balance < amount:
                raise ValueError("Error: Insufficient funds!")
        
            connection.autocommit = False

            # Perform a balance check on the wallet
            cursor.execute("SELECT balance FROM users WHERE wallet_id = %s", (wallet_id))
            wallet_balance = cursor.fetchone()
            if not wallet_balance:
                raise ValueError("Error: Wallet not found!")
            if not wallet_id:
                raise ValueError("Wallet not found!")
            
            # Subtract funds from the wallet
            cursor.execute(
                "UPDATE users SET wallet_balance = balance - %s WHERE wallet_id = %s", (wallet_id, amount)
            )

            # Add funds to the account
            cursor.execute(
                "UPDATE users SET account_balance = balance + %s WHERE account_number = %s", (account_id, amount)
            )

            #Log the transaction
            cursor.execute(
                """
                INSERT INTO transactions (wallet_id, account_id, amount, transaction_id)
                VALUES (%s, %s, %s, %s, %s)
                """, (wallet_id, account_id, amount, transaction_id, 'Completed!')
            )
            connection.commit()
            print("Successfully deposited funds!")
            cls.send_kafka_deposit_to_account_update(account_id, wallet_id, amount, transaction_id)

        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            print("Error: Transaction failed", error)
        finally:
            cursor.close()
            connection.close()


    def send_deposit_to_account_update(user_email, account_id, wallet_id, transaction_id):
        """Sends an update to the appropriate Kafka topic for every deposit"""
        transaction_data = {
            "user_email": user_email,
            "account_id": account_id,
            "wallet_id": wallet_id,
            "transaction_id": transaction_id
        }
        kafka_instance.send_deposit_to_account_update(transaction_data)