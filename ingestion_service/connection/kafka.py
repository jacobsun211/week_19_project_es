import os
from confluent_kafka import Producer


class KafkaConnection:
    def __init__(self):
        SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.producer = Producer({"bootstrap.servers": SERVER})


producer = KafkaConnection().producer
