from confluent_kafka import Consumer, Producer
from elastic_consumer.models import ImageData
import json
import os
from confluent_kafka import Producer
import logging
from shared.logging_config import configure_logging
from shared.models import ImageData


configure_logging("elastic_consumer.main")
logger = logging.getLogger(__name__)


SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
producer = Producer({"bootstrap.servers": SERVER})



LISTENS_TOPIC1  = os.getenv("ELASTIC_CONSUMER_LISTENING_TOPIC1", "RAW")
LISTENS_TOPIC2  = os.getenv("ELASTIC_CONSUMER_LISTENING_TOPIC2", "clean")
LISTENS_TOPIC3  = os.getenv("ELASTIC_CONSUMER_LISTENING_TOPIC3", "analytics")

# WRITING_TOPIC  = os.getenv("ELASTIC_CONSUMER_WRITING_TOPIC", "analytics")

conf = {
    'bootstrap.servers': SERVER,
    'group.id': "elastic",
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)


consumer.subscribe([LISTENS_TOPIC1, LISTENS_TOPIC2, LISTENS_TOPIC3])


from elastic_consumer.connection import insert
while True:
    image = consumer.poll(1.0)
    if image is None: continue
    if image.error():
        print(f"elastic error: {image.error()}")
        continue
    image = json.loads(image.value()) # from str to dict
    image = ImageData(**image) # from dict to class object
    insert(image)
    print('noice')
    
    # if msg.topic() == "RAW":
    #     handle_raw(msg)
    # elif msg.topic() == "clean":
    #     handle_clean(msg)
    # elif msg.topic() == "analytics":
    #     handle_analytics(msg)





# python -m elastic_consumer.main


clean()





# image: docker.elastic.co/elasticsearch/elasticsearch:8.12.0
# pip install "elasticsearch<9.0.0"

