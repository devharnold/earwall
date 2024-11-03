from kafka import KafkaProducer
import json

class KafkaProducerInstance:
    """
    Handles all kafka producer operations
    """
    def __init__(self, kafka_topic):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.kafka_topics = {
            "p2p_transfer": "p2p_transfer_notifications",
            "withdraw": "withdraw_from_account_notifications",
            "deposit": "deposit_notifications",
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
            print(f"nvalid transaction type: {transaction_type}")