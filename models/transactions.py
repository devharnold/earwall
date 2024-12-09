#!/usr/bin/env python3

"""Transaction model class"""

import psycopg2
from psycopg2 import sql
from models.baseModel import BaseModel
import os
from flask import jsonify
import requests
from decimal import Decimal
from kafka_ms.kafka_producer import KafkaProducerInstance
from engine.db_storage import get_db_connection
from dotenv import load_dotenv
load_dotenv()


kafka_instance = KafkaProducerInstance()

class Transaction(BaseModel):
    """Transaction model"""
    def __init__(self, user_email: str, sender_user_id: int, receiver_user_id: int, sender_cw_id: int, receiver_cw_id: int, amount: float, transaction_id: str):
        self.user_email = user_email
        self.sender_user_id = sender_user_id
        self.receiver_user_id = receiver_user_id
        self.sender_cw_id = sender_cw_id
        self.receiver_cw_id = receiver_cw_id
        self.amount = amount
        self.transaction_id = transaction_id

    @classmethod
    def process_p2p_transaction(cls, user_email, sender_user_id, receiver_user_id, sender_cw_id, receiver_cw_id, amount, transaction_id, sender_currency, receiver_currency):
        """Initiates a transaction between two users in a p2p eft service with currency conversion."""
        try:
            conn=get_db_connection()
            cursor=conn.cursor()

            if amount <= 0:
                return jsonify({"error": "You cannot transact 0 funds" }), 400
            
            # Prevents from performing an auto-commit
            conn.autocommit = False

            cursor.execute("SELECT balance, currency FROM cashwallets WHERE cashwallet_id = %s", (sender_cw_id,))
            sender_data = cursor.fetchone()
            if sender_data is None:
                return jsonify({"error": "Sender wallet not found."}), 404
            sender_balance, sender_currency = sender_data
            sender_balance = Decimal(sender_balance)

            if sender_balance < amount:
                return jsonify(({"error": "Insufficient funds in your wallet!"})), 400
            
            if sender_currency != receiver_currency:
                amount = cls.convert_currency(amount, sender_currency, receiver_currency)
            
            cursor.execute("UPDATE users SET balance = balance - %s WHERE cashwallet_id = %s", (amount, sender_cw_id))
            cursor.execute("UPDATE users SET balance = balance + %s WHERE cashwallet_id = %s", (amount, receiver_cw_id))

            #Log the transaction
            cursor.execute(
                """
                INSERT INTO transactions (sender_user_id, receiver_user_id, sender_cw_id, receiver_cw_id, amount, transaction_type, transaction_id, sender_currency, receiver_currency)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING transaction_id
                """,
                (sender_user_id, receiver_user_id, sender_cw_id, receiver_cw_id, amount, 'P2P Transfer', transaction_id, sender_currency, receiver_currency)
            )
            transaction_id = cursor.fetchone()[0]
            conn.commit()

            # notify via kafka
            cls.send_kafka_p2p_transfer_update(user_email, sender_cw_id, receiver_cw_id, amount, transaction_id)

            # Return a message
            return jsonify({"message": "Transaction Completed successfully", "transaction_id": transaction_id}), 201
        
        except Exception as e:
            conn.rollback() # After an unsuccessful connection
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def convert_currency(cls, amount: float, from_currency: str, to_currency: str) -> float:
        """Converts an amount from one currency to another"""
        if from_currency == to_currency:
            return amount
        
        #fetch the exchange rate and perform the currency conversion
        exchange_rate = cls.get_exchange_rate(from_currency, to_currency)
        return amount * exchange_rate
    
    @classmethod
    def get_exchange_rate(cls, from_currency: str, to_currency: str) -> float:
        """Fetch exchang rate between the two currencies involved"""
        url=f""
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get("result") == "success":
            exchange_rate = data['conversion_rates'].get(to_currency)
            if exchange_rate:
                return exchange_rate
            else:
                raise ValueError(f"Exchange rate not available for {to_currency}")
        else:
            raise ValueError("Failed to fetch the exchange rates")

    @classmethod
    def withdraw_from_account(cls, account_id, balance: float, cashwallet_id, amount, transaction_id):
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
            
            if not cashwallet_id:
                raise ValueError("Wallet not found!")
            
            # Subtract funds from the account to the wallet
            cursor.execute(
                "UPDATE users SET account_balance = balance - %s WHERE account_number = %s", (account_id, amount)
            )
            
            # Add funds to the wallet
            cursor.execute(
                "UPDATE users SET wallet_balance = balance + %s WHERE cashwallet_id = %s", (cashwallet_id, amount)
            )

            # Log that transaction activity
            cursor.execute(
                """
                INSERT INTO transactions (account_id, cashwallet_id, amount, transaction_type, status)
                VALUES (%s, %s, %s, %s, %s)
                """, (account_id, cashwallet_id, amount, 'Completed')
            )
            conn.commit()
            print("Withdrawal successful.")
            cls.send_kafka_withdraw_transfer_update(account_id, cashwallet_id, amount, transaction_id)
        except (Exception, psycopg2.DatabaseError) as error:
            conn.rollback()
            print("Transaction failed. Error!:", error)
        finally:
            cursor.close()
            conn.close()
            
    @classmethod
    def deposit_to_account(cls, amount, account_id, cashwallet_id, transaction_id):
        """deposit funds from the wallet to your account."""
        try:
            conn=get_db_connection()
            cursor=conn.cursor()

            if wallet_balance < amount:
                raise ValueError("Error: Insufficient funds!")
        
            conn.autocommit = False

            # Perform a balance check on the wallet
            cursor.execute("SELECT balance FROM users WHERE cashwallet_id = %s", (cashwallet_id))
            wallet_balance = cursor.fetchone()
            if not wallet_balance:
                raise ValueError("Error: Wallet not found!")
            if not cashwallet_id:
                raise ValueError("Wallet not found!")
            
            # Subtract funds from the wallet
            cursor.execute(
                "UPDATE users SET wallet_balance = balance - %s WHERE cashwallet_id = %s", (cashwallet_id, amount)
            )

            # Add funds to the account
            cursor.execute(
                "UPDATE users SET account_balance = balance + %s WHERE account_number = %s", (account_id, amount)
            )

            #Log the transaction
            cursor.execute(
                """
                INSERT INTO transactions (cashwallet_id, account_id, amount, transaction_id)
                VALUES (%s, %s, %s, %s, %s)
                """, (cashwallet_id, account_id, amount, transaction_id, 'Completed!')
            )
            conn.commit()
            print("Successfully deposited funds!")
            cls.send_kafka_deposit_to_account_update(account_id, cashwallet_id, amount, transaction_id)

        except (Exception, psycopg2.DatabaseError) as error:
            conn.rollback()
            print("Error: Transaction failed", error)
        finally:
            cursor.close()
            conn.close()