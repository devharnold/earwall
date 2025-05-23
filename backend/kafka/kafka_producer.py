#!/usr/bin/env python3
"""Kafka producer class"""

from kafka import KafkaProducer
from backend.email_ms.send_transmail import EmailTransactionService
from backend.email_ms.send_regmail import RegularEmailService
import json

class KafkaProducerInstance:
    """
    Handles all kafka producer operations
    """
    def __init__(self, topics):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topics = {
            #label: topic --> Key, value pair.
            "p2p_transaction": "wallet_transactions_notifications",
            "withdraw": "withdraw_from_cash_wallet_notifications",
            "deposit": "deposit_notifications",
            "paypal_config": "paypal_config_notification",
            "transfer_to_paypal": "transfer_to_paypal_notifications",
            "transfer_from_paypal": "transfer_from_paypal_notifications"
        }

    def send_update(self, transaction_data, transaction_type):
        """Sends transaction data to the appropriate kafka topic"""
        topic = self.kafka_topics.get(transaction_type)
        if topic:
            try:
                self.producer.send(topic, transaction_data)
                self.producer.flush()
                print(f"{transaction_type} update sent to Kafka topic '{topic}'.")
            except Exception as e:
                print(f"Error sending to Kafka topic '{topic}': {e}")
        else:
            print(f"Invalid transaction type: {transaction_type}")