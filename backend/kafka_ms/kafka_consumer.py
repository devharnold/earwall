#!/usr/bin/env python3

"""Multi-threaded kafka consumer function."""
from kafka import KafkaConsumer
import json
import threading
from email_ms.send_transmail import EmailTransactionService
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

class KafkaConsumerHandler:
    """Generic Kafka consumer handler for processing messages from a specific topic
    """
    def __init__(self, topic, group_id):
        load_dotenv()

        """Initialization of the kafka consumer functions"""
        self.topic = topic
        self.bootstrap_servers = ['localhost:9092']
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id=group_id,
            auto_offset_reset="earliest"
        )

        # initialize the email service
        self.email_service = EmailTransactionService(
            sender_email=os.getenv("SENDER_EMAIL"),
            password=os.getenv("SENDER_EMAIL_PASSWORD"),
            smtp_server=os.getenv("SMTP_SERVER"),
            port=int(os.getenv("SMTP_PORT", 587))
        )

    def consume_messages(self):
        """Consumer for wallet notifications. Listens to kafka topic and processes messages"""
        try:
            print(f"Listening to kafka topic: {self.topic}")
            for message in self.consumer:
                user_email = message.value.get("user_email")
                message_body = message.value.get("message_body")

                if not user_email or not message_body:
                    print("Invalid message format received. Skipping...")
                    continue

                self.email_service.send_email(user_email, message_body)
                print(f"Notification sent to {user_email} regarding {message_body}")
        except Exception as e:
            print("Error while consuming messages: {e}")
        finally:
            self.consumer.close()

    def run_consumers(topics):
        threads = []
        for topic, group_id in topics.items():
            consumer = KafkaConsumerHandler(topic, group_id)
            thread = threading.Thread(target=consumer.consume_messages)
            thread.start()
            threads.append(thread)

        for threads in threads:
            thread.join()

if __name__ == "__main__":
    topics = {
        "wallet-trasnactions-notifications": "cash_wallet_group",
        "withdrawal-notifications": "withdrawal_group",
        "deposit-notifications": "deposit_group",
        "paypal-config-notifications": "paypal_config_group",
        "payment-to-paypal-notifications": "paypal_payment_group",
        "payment-from-paypal-notifications": "paypal_payment_group",
    }
    
    try:
        KafkaConsumerHandler.run_consumers(topics)
    except KeyboardInterrupt:
        logging.info("Shutting down consumers...")