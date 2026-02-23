
from confluent_kafka import Consumer, Producer
from models import ImageData
import json
import time
import os
from confluent_kafka import Producer



SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
producer = Producer({"bootstrap.servers": SERVER})






WRITING_TOPIC = "clean"
LISTENS_TOPIC = "RAW"

conf = {
    'bootstrap.servers': SERVER,
    'group.id': "cleaning consumer",
    'auto.offset.reset': 'earliest'
}



consumer = Consumer(conf)
consumer.subscribe([LISTENS_TOPIC])

def send_to_kafka(image):
        #                           ! since its a class object, we need to convert it to dict and THEN to str
        image = json.dumps(image.__dict__).encode('utf-8')
        producer.produce(WRITING_TOPIC, image)
        producer.poll(0)
        print(image)
        


def clean():
    while True:
            image = consumer.poll(1.0) 
            if image is None: continue
            if image.error():
                print(f"cleaner error: {image.error()}")
                continue


            image = json.loads(image.value()) # from str to dict
            image = ImageData(**image) # from dict to class object
            image.text = image.text.replace("\x0c", "").replace("?", "").replace("!", "").strip().lower() # cleaning the text
            send_to_kafka(image)
         
clean()