#!/usr/bin/env python3
"""Kafka producer class"""

from kafka import KafkaProducer
import json

class WalletTransactionNotificationProducer:
    """
    Handles all kafka producer operations
    """
    def __init__(self, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = {
            #label: topic --> Key, value pair.
            "wallet-transfer": "wallet_transactions_notifications",
        }

    def send_update(self, transaction_data, transaction_id):
        """Sends transaction data to the appropriate kafka topic"""
        topic = self.kafka_topics.get(transaction_id)
        if topic:
            try:
                self.producer.send(topic, transaction_data)
                self.producer.flush()
                print(f"{transaction_id} update sent to Kafka topic '{topic}'.")
            except Exception as e:
                print(f"Error sending to Kafka topic '{topic}': {e}")
        else:
            print(f"Invalid transaction type: {transaction_id}")