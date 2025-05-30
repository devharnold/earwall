import os
import json
import logging
from kafka import KafkaConsumer
from dotenv import load_dotenv
from backend.email_ms.creditWallet import EmailCreditWallet

load_dotenv()
logging.basicConfig(level=logging.INFO)

def run_wallet_credit_consumer():
    topic = "wallet-credit"
    group_id = "wallet_credit_group"
    kafka_server = os.getenv("KAFKA_BROKER", "localhost:9092")

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_server,
        value_desirializer=lambda m: json.loads(m.decode("utf-8")),
        group_id=group_id,
        auto_offset_reset="earliest",
    )

    email_service = EmailCreditWallet()

    try:
        logging.info(f"[{topic}] Listening for credit email events...")
        for message in consumer:
            payload = message.value
            user_email = payload.get("user_email")
            amount = payload.get("amount")
            transaction_id = payload.get("transaction_id")

            if not user_email or not amount:
                logging.warning(f"Invalid message payload")
                continue

            email_service.send_email(user_email)
            logging.info(f"[{topic}] Credit email sent to {user_email}")
    except Exception as e:
        logging.error(f"[{topic}] Error: {e}")
    finally:
        consumer.close()