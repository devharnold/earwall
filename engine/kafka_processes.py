from kafka import KafkaProducer
import json

class KafkaProcesses:
    """Handles all kafka processes including notification streaming"""
    def __init__(self, kafka_topic):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.kafka_topics = {
            "withdraw": "withdraw_from_account_notifications",
            "deposit": "deposit_notifications",
            "transfer_to_paypal": "transfer_to_paypal_notifications",
            "transfer_from_paypal": "transfer_from_paypal_notifications"
        }

    def send_withdraw_update(self, transaction_data):
        """sends a transaction update to kafka on 'withdraw_from_account_notifications' topic"""
        self.producer.send(self.kafka_topics["withdraw"], transaction_data)
        self.producer.flush()

    def send_deposit_update(self, transaction_data):
        """sends a transaction update to kafka on 'deposit_to_account' notifications"""
        self.producer.send(self.kafka_topics["deposit"], transaction_data)
        self.producer.flush()
    
    def send_paypal_transfer_update(self, transaction_data):
        """sends a paypal transfer update to kafka on 'transfer_to_paypal_notifications' topic"""
        self.producer.send(self.kafka_topics["transfer_to_paypal"], transaction_data)
        self.producer.flush()

    def send_