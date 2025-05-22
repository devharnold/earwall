#!/usr/bin/env python3

import os
import json
import threading
import logging
import time
from kafka import KafkaConsumer
from dotenv import load_dotenv
from backend.email_ms.send_transmail import EmailTransactionService

load_dotenv()
logging.basicConfig(level=logging.INFO)


class SupervisedThread(threading.Thread):
    """
    A thread that supervises and restarts the Kafka consumer on failure.
    """
    def __init__(self, topic, group_id):
        super().__init__()
        self.topic = topic
        self.group_id = group_id
        self.daemon = True

    def run(self):
        while True:
            try:
                logging.info(f"[{self.topic}] Starting consumer ...")
                consumer = KafkaConsumerHandler(self.topic, self.group_id)
                consumer.consume_messages()
            except Exception as e:
                logging.error(f"[{self.topic}] Error: {e}")
                time.sleep(5)  # backoff before restart


class KafkaConsumerHandler:
    """
    Handles consumption of Kafka messages from a specific topic.
    """

    def __init__(self, topic, group_id):
        self.topic = topic
        self.group_id = group_id
        self.bootstrap_servers = os.getenv("KAFKA_BROKER", "localhost:9092")

        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id=self.group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=True
        )

        self.email_service = EmailTransactionService(
            sender_email=os.getenv("SENDER_EMAIL"),
            password=os.getenv("SENDER_EMAIL_PASSWORD"),
            smtp_server=os.getenv("SMTP_SERVER"),
            port=int(os.getenv("SMTP_PORT", 587))
        )

    def consume_messages(self):
        logging.info(f"[{self.topic}] Listening for messages...")
        try:
            for message in self.consumer:
                payload = message.value
                user_email = payload.get("user_email")
                message_body = payload.get("message_body")

                if not user_email or not message_body:
                    logging.warning(f"[{self.topic}] Invalid message: {payload}")
                    continue

                self.email_service.send_email(user_email, message_body)
                logging.info(f"[{self.topic}] Email sent to {user_email}")
        except Exception as e:
            logging.error(f"[{self.topic}] Consumer failed: {e}")
            raise
        finally:
            self.consumer.close()

    @staticmethod
    def run_consumers(topic_group_map):
        threads = []
        for topic, group_id in topic_group_map.items():
            thread = SupervisedThread(topic, group_id)
            thread.start()
            threads.append(thread)

        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            logging.info("Shutting down consumers...")


if __name__ == "__main__":
    topic_group_map = {
        "wallet-debit": "wallet_debit_group",
        "wallet-credit": "wallet_credit_group"
    }

    KafkaConsumerHandler.run_consumers(topic_group_map)
