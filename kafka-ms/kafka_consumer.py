from kafka import KafkaConsumer
import json
from models.user import User
from models.wallets.cashwallet import CashWallet
from email_ms.send_transmail import EmailTransactionService, send_email_notification
import os
from dotenv import load_dotenv

class KafkaConsumerFunction:
    """Kafka consumer function for respective models
    Params:
        cwts - cash_wallet_transactions
    """
    def __init__(self):
        load_dotenv()

        """Initialization of the kafka consumer functions"""
        self.topic = 'wallet-transactions-notifications'
        self.bootstrap_servers = ['localhost:9092']
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            group_id="wallet_transactions_group",
            auto_offset_reset="earliest"
        )

        # initialize the email service
        self.email_service = EmailTransactionService(
            sender_email=os.getenv("SENDER_EMAIL"),
            password=os.getenv("SENDER_EMAIL_PASSWORD"),
            smtp_server=os.getenv("SMTP_SERVER"),
            port=int(os.getenv("SMTP_PORT", 587))
        )

    def consume_email_notifications(self, user_email):
        """Consumer for wallet notifications. Listens to kafka topic and processes messages"""
        try:
            for message in self.consumer:
                # extract the message fields
                user_email = message.value.get("user_email")
                message_body = message.value.get("message_body")

                if not user_email or not message_body:
                    print("Invalid message format received, skipping")
                    continue

                self.email_service.send_email_notification(user_email, message_body) # send email using the email service
                print(f"Notification sent to {user_email} regarding {message_body}")
        except Exception as e:
            print(f"Error while consuming messages: {e}")
        finally:
            self.consumer.close()