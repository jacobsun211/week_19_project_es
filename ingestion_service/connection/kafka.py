import os
from confluent_kafka import Producer



SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


producer = Producer({"bootstrap.servers": SERVER})