#!/usr/bin/env python3

"""Transaction model class"""

import psycopg2
from psycopg2 import sql
from models.wallets import CashWallet
import os
from flask import jsonify, request
from kafka import KafkaProducer, KafkaConsumer
from engine.kafka_processes import KafkaProcesses
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

kafka_instance = KafkaProcesses()

class Transaction(CashWallet):
    """Transaction model"""
    def __init__(self, user_email: str, sender_wallet, receiver_wallet, amount, transaction_type, status='Pending'):
        self.sender_account = sender_wallet
        self.receiver_account = receiver_wallet
        self.amount = amount
        self.transaction_type = transaction_type
        self.status = status

    #kafka_topics = 'transaction_notifications'
    #producer = KafkaProducer(
    #    bootstrap_servers=['localhost:9092'],
    #    value_serializer=lambda v: json.dumps(v).encode('utf-8')
    #)

    @classmethod
    def process_p2p_transaction(cls, wallet_type: str, user_email: str, sender_wallet: str, receiver_wallet, amount, transaction_type, transaction_id):
        """Initiates a transaction to take place between different accounts, an p2p eft service."""
        try:
            connection = psycopg2.connect(
                dbname=DB_NAME,
                dbhost=DB_HOST,
                dbport=DB_PORT,
                dbuser=DB_USER,
                dbpassword=DB_PASSWORD
            )
            cursor = connection.cursor()

            if amount <= 0:
                return jsonify({"error": "You cannot transact 0 funds" }), 400
            
            # Prevents from performing an auto-commit
            connection.autocommit = False

            cursor.execute("SELECT balance FROM users WHERE wallet_id = %s", (sender_wallet))
            sender_balance = cursor.fetchone()
            if sender_balance is None:
                return jsonify({"error": "Sender wallet not found."}), 404
            sender_balance = sender_balance[0]

            if sender_balance < amount:
                return jsonify(({"error": "Insufficient funds in your wallet!"})), 400
            
            cursor.execute("""
                           INSERT INTO transactions (sender_wallet, receiver_wallet, amount, transaction_type, status)
                           VALUES (%s, %s, %s, %s, %s) RETURNING id
                           """, (sender_wallet, receiver_wallet, amount, transaction_type, 'Pending'))
            transaction_id = cursor.fetchone()

            cursor.execute("""
                           UPDATE users SET balance - %s WHERE wallet_id =%s
                           """, (amount, user_email, sender_wallet)
                           )
            
            cursor.execute("""
                           UPDATE users SET balance + %s WHERE wallet_id =%s
                           """, (amount, user_email, receiver_wallet))
            connection.commit()

            cls.producer.send(cls.kafka_topic, {
                "user_email": user_email,
            })
            return jsonify({"message": "Updated"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def update_after_p2p_transactions(cls, sender_wallet, receiver_wallet, amount, transaction_type):
        try:
            connection = psycopg2.connect(
                dbname=DB_NAME,
                dbhost=DB_HOST,
                dbport=DB_PORT,
                dbuser=DB_USER,
                dbpassword=DB_PASSWORD
            )
            cursor = connection.cursor()

            # Begin the transaction.
            connection.autocommit = False

            # Check the senders balance.
            cursor.execute("SELECT balance FROM users WHERE wallet_id =%s," (sender_wallet))
            sender_balance = cursor.fetchone()
            if not sender_balance:
                raise ValueError("Sender wallet does not exist!")
            
            if sender_balance < amount:
                raise ValueError("!Insufficient funds!")
            
            # Subtract amount from sender's balance...
            cursor.execute(
                "UPDATE users SET balance = balance - %s WHERE wallet_id = %s", (sender_wallet, amount)
            )

            # Add amount to receiver's balance...
            cursor.execute(
                "UPDATE users SET balance = balance + %s WHERE wallet_id = %s", (receiver_wallet, amount)
            )

            #Log transaction
            cursor.execute(
                """
                INSERT INTO transactions (sender_wallet, receiver_wallet, amount, transaction_type, status)
                VALUES (%s, %s, %s, %s, %s)
                """, (sender_wallet, receiver_wallet, amount, transaction_type, 'Completed')
            )
            connection.commit()
            print("Transaction completed successfully.")

        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback() #Incase of an error, rollback!
            print("Transaction Failed Error: ", error)

        finally:
            cursor.close()
            connection.close()

    @classmethod
    def withdraw_from_account(cls, account, balance, wallet_id, amount, transaction_type, status):
        try:
            connection = psycopg2.connect(
                dbname = DB_NAME,
                dbport = DB_PORT,
                dbhost = DB_HOST,
                dbpassword = DB_PASSWORD,
                dbuser = DB_USER 
            )
            cursor = connection.cursor()

        # Perform the balance check on the user's account.
            if balance < amount:
                return jsonify({"error": "You cant withdraw. You don't have funds!"}), 400

            connection.autocommit = False

            # Perform a balance check from the user's account
            cursor.execute("SELECT balance FROM users WHERE account_number = %s", (account))
            account_balance = cursor.fetchone()
            if not account_balance:
                raise ValueError("Account does not exist!!!")
            
            if account_balance < amount:
                raise ValueError("Insufficient funds. Cannot perform action!")
            
            if not wallet_id:
                raise ValueError("Wallet not found!")
            
            # Subtract funds from the account to the wallet
            cursor.execute(
                "UPDATE users SET account_balance = balance -%s WHERE account_number = %s", (account, amount)
            )
            
            # Add funds to the wallet
            cursor.execute(
                "UPDATE users SET wallet_balance = balance + %s WHERE wallet_id = %s", (wallet_id, amount)
            )

            # Log that transaction activity
            cursor.execute(
                """
                INSERT INTO transactions (account, wallet_id, amount, transaction_type, status)
                VALUES (%s, %s, %s, %s, %s)
                """, (account, wallet_id, amount, transaction_type, 'Completed')
            )
            connection.commit()
            print("Withdrawal successful.")

        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            print("Transaction failed. Error!:", error)

        finally:
            cursor.close()
            connection.close()

    @classmethod
    def deposit_to_account(cls, amount, wallet_balance, account_id, wallet_id, transaction_type, status):
        try:
            connection = psycopg2.connect(
                dbname= DB_NAME,
                dbuser=DB_USER,
                dbport=DB_PORT,
                dbhost=DB_HOST,
                dbpassword=DB_PASSWORD
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
                INSERT INTO transactions (wallet_id, account, amount, transaction_type, status)
                VALUES (%s, %s, %s, %s, %s)
                """, (wallet_id, account_id, amount, transaction_type, 'Completed!')
            )
            connection.commit()
            print("Successfully deposited funds!")

        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            print("Error: Transaction failed", error)
        finally:
            cursor.close()
            connection.close()


    def send_email_notification(user_email, transaction_state)
    
