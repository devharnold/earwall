#!/usr/bin/env python3

"""Transaction model class"""

import psycopg2
from psycopg2 import sql
from models.baseModel import BaseModel
from models.wallets import CashWallet
import os
from flask import jsonify, request
from kafka_ms.kafka_producer import KafkaProducerInstance
from engine.db_storage import get_db_connection


kafka_instance = KafkaProducerInstance()

class Transaction(BaseModel):
    """Transaction model"""
    def __init__(self, user_email: str, sender_wallet_id: int, receiver_wallet_id: int, amount: float, transaction_id: str):
        self.user_email = user_email
        self.sender_wallet_id = sender_wallet_id
        self.receiver_wallet_id = receiver_wallet_id
        self.amount = amount
        self.transaction_id = transaction_id

    @classmethod
    def process_p2p_transaction(cls, user_email: str, sender_wallet_id, receiver_wallet_id, amount, transaction_id: str):
        """Initiates a transaction to take place between different accounts, an p2p eft service."""
        try:
            conn=get_db_connection()
            cursor=conn.cursor()

            if amount <= 0:
                return jsonify({"error": "You cannot transact 0 funds" }), 400
            
            # Prevents from performing an auto-commit
            conn.autocommit = False

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
            conn.commit()

            # notify via kafka
            cls.send_kafka_p2p_transfer_update(user_email, sender_wallet_id, receiver_wallet_id, amount, transaction_id)

            # Return a message
            return jsonify({"message": "Transaction Completed successfully", "transaction_id": transaction_id}), 201
        
        except Exception as e:
            conn.rollback() # After an unsuccessful connection
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def withdraw_from_account(cls, account_id, balance: float, wallet_id, amount, transaction_id):
        try:
            conn=get_db_connection()
            cursor=conn.cursor()

        # Perform the balance check on the user's account.
            if balance < amount:
                return jsonify({"error": "You cant withdraw. You don't have funds!"}), 400

            conn.autocommit = False

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
                "UPDATE users SET account_balance = balance - %s WHERE account_number = %s", (account_id, amount)
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
                """, (account_id, wallet_id, amount, 'Completed')
            )
            conn.commit()
            print("Withdrawal successful.")
            cls.send_kafka_withdraw_transfer_update(account_id, wallet_id, amount, transaction_id)


        except (Exception, psycopg2.DatabaseError) as error:
            conn.rollback()
            print("Transaction failed. Error!:", error)

        finally:
            cursor.close()
            conn.close()

    @classmethod
    def deposit_to_account(cls, amount, account_id, wallet_id, transaction_id):
        """deposit funds from the wallet to your account."""
        try:
            conn=get_db_connection()
            cursor=conn.cursor()

            if wallet_balance < amount:
                raise ValueError("Error: Insufficient funds!")
        
            conn.autocommit = False

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
            conn.commit()
            print("Successfully deposited funds!")
            cls.send_kafka_deposit_to_account_update(account_id, wallet_id, amount, transaction_id)

        except (Exception, psycopg2.DatabaseError) as error:
            conn.rollback()
            print("Error: Transaction failed", error)
        finally:
            cursor.close()
            conn.close()