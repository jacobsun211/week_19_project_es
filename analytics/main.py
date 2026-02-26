from confluent_kafka import Consumer, Producer
from shared.models import ImageData
import json
import os
from confluent_kafka import Producer
import logging
from shared.logging_config import configure_logging

configure_logging("analytics.main")
logger = logging.getLogger("analytics.main")


SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
producer = Producer({"bootstrap.servers": SERVER})



LISTENS_TOPIC  = os.getenv("ANALYTICS_LISTENING_TOPIC", "clean")
WRITING_TOPIC  = os.getenv("ANALYTICS_WRITING_TOPIC", "analytics")

conf = {
    'bootstrap.servers': SERVER,
    'group.id': "analytics",
    'auto.offset.reset': 'earliest'
}



consumer = Consumer(conf)
consumer.subscribe([LISTENS_TOPIC])

def send_to_kafka(image: ImageData):
        #                           ! since its a class object, we need to convert it to dict and THEN to str
        analyzed = json.dumps(image.__dict__).encode('utf-8')
        producer.produce(WRITING_TOPIC, analyzed)
        producer.poll(0)
        logger.info(f"Sent image '{image.imageName}' to topic '{WRITING_TOPIC}'")
        


def clean():
    while True:
            image = consumer.poll(1.0) 
            if image is None: continue
            if image.error():
                print(f"cleaner error: {image.error()}")
                continue


            image = json.loads(image.value()) # from str to dict
            image = ImageData(**image) # from dict to class object
            print(image.text)
            print(type(image.text))
            print(len(image.text))
            for i in len(image.text):
                  print(i)
            # image.text = image.text.replace("\x0c", "").replace("?", "").replace("!", "").strip().lower() # cleaning the text
            send_to_kafka(image)
         
clean()


# python -m analytics.main

