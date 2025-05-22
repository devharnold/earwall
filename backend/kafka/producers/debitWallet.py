from kafka import KafkaProducer
import json

class DebitWalletNotificationProducer:
    def __init__(self, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = {
            "wallet-debit": "wallet_debit_notifications"
        }

    def send_updates(self, transaction_data, transaction_type):
        topic = self.kafka_topics.get(transaction_type)
        if topic:
            try:
                self.producer.send(topic, transaction_data)
                self.producer.flush()
                print(f"{transaction_type} update sent to Kafka topic '{topic}'.")
            except Exception as e:
                print(f"Error sending to kafka topic '{topic}': {e}")
        else:
            print(f"Invalid transaction_type: {transaction_type}")