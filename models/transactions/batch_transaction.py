"""Batch Transaction model class"""

import os
from flask import jsonify
from models.baseModel import BaseModel
from rgsync import RGJSONWriteBehind, RGJSONWriteThrough
from rgsync.Connectors import PostgresConnector, PostgresConnection
from kafka import KafkaProducer, KafkaClient
import uuid
import requests
from decimal import Decimal
from engine.db_storage import get_db_connection
from dotenv import load_dotenv
load_dotenv()

connection = PostgresConnection('root', 'password', 'host')

'''Create postgres transactions connector'''
transactionsConnector = PostgresConnector(connection, 'transactions', 'id')

transactionsMappings = {
    'sender_user_id': 'sender_user_id',
    'reciever_user_id': 'receiver_user_id',
    'from_currency': 'from_currency',
    'to_currency': 'to_currency',
    'cashwallet_id': 'cashwallet_id',
    'amount': 'amount',
}

RGJSONWriteThrough(keysPrefix='__', mappings=transactionsMappings)


class BatchTransaction(BaseModel):
    """Batch Transaction Model"""
    def __init__(self, sender_user_id, recievers, from_currency, to_currency, transaction_id, amount):
        self.sender_user_id = sender_user_id
        self.reciever_user_id = recievers
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.amount = amount
        self.transaction_id = self.generate_transaction_id()

    @classmethod
    def process_batch_transactions(cls, b_transactions):
        available_currencies = ["GBP", "USD", "KES"]

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            connection.autocommit = False

            results = []

            for b_transaction in b_transactions:
                sender_user_id = b_transaction['sender_user_id']
                receivers = b_transaction['receivers']
                from_currency = b_transaction['from_currency']
                to_currency = b_transaction['to_currency']
                amount = b_transaction['amount']
                transaction_id = b_transaction['transaction_id']

                while sender_user_id:
                    if amount <= 0:
                        results.append({"transaction_id": transaction_id, "status": " Failed. Insufficient funds"})
                        continue

                    if from_currency not in available_currencies and to_currency not in available_currencies:
                        results.append({"transaction_id": transaction_id, "status": "Failed. Currency not available."})
                        continue

                cursor.execute("SELECT balance FROM cashwallets WHERE cashwallet_id = %s", (sender_user_id,))
                sender_data = cursor.fetchone()
                if not sender_data:
                    results.append({"transaction_id": transaction_id, "status": "Sender wallet not found"})
                    continue

                sender_balance = sender_data[0]
                if sender_balance < amount:
                    results.append({"transaction_id": transaction_id, "status": "Insufficient funds in your wallet"})
                    continue

                for receiver in receivers:
                    receiver_user_id = receiver['receiver_user_id']
                    receiver_amount = receiver['amount']
                    receiver_transaction_id = receiver['transaction_id']

                    cursor.execute(
                        """
                        INSERT INTO transactions (sender_user_id, receiver_user_id, amount, from_currency, to_currency, transaction_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (sender_user_id, receiver_user_id, from_currency, to_currency, amount, transaction_id)
                    )
                    sender_balance -= receiver_amount # Deduct the balance from sender's wallet to the receivers' wallets
                    results.append({"transaction_id": receiver_transaction_id, "status": "Transaction Complete"})
            
            connection.commit()
            return results
        except Exception as e:
            connection.rollback()
            return {"error": "Batch process failed", "message": str(e)}, 500
        finally:
            connection.close()
            cursor.close()