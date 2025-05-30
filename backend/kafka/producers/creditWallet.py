from kafka import KafkaProducer
import json

class CreditWalletProducer:
    def __init__(self, topic):
        self.producer = KafkaProducer(
            bootstrap_servers = ['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = {
            "wallet-credit": "wallet_credit_notifications"
        }

    def send_updates(self, transaction_data, transaction_id):
        topic = self.kafka_topics.get(transaction_id)
        if topic:
            try:
                self.producer.send(topic, transaction_id)
                self.producer.flush()
                print(f"{transaction_id} update sent to Kafka Topic '{topic}'.")
            except Exception as e:
                print(f"Error sending info to Kafka Topic '{topic}': {e}")
            else:
                print(f"Invalid transaction_id: {transaction_id}")