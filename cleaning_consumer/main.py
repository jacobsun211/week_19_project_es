from confluent_kafka import Consumer, Producer
from shared.models import CleanedData
import json
import os
from confluent_kafka import Producer
import re
from nltk.corpus import stopwords #
from nltk.tokenize import word_tokenize #
import logging
from shared.logging_config import configure_logging
configure_logging("cleaning_consumer.main")                                               
#                              ! the name of the file -> 2026-02-24 10:08:41,733 [INFO] __main__ - Sent image 'tweet_9.png' to topic 'clean'
# logger = logging.getLogger(__name__)                                                  !!!!!!!!  
logger = logging.getLogger("cleaning_consumer.main")



SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
producer = Producer({"bootstrap.servers": SERVER})





WRITING_TOPIC = os.getenv("CLEANING_WRITING_TOPIC", "clean")
LISTENS_TOPIC = os.getenv("CLEANING_LISTENING_TOPIC", "RAW")


conf = {
    'bootstrap.servers': SERVER,
    'group.id': "cleaning consumer",
    'auto.offset.reset': 'earliest'
}



consumer = Consumer(conf)
consumer.subscribe([LISTENS_TOPIC])

# nltk.download('punkt_tab') run only once!
# nltk.download('stopwords')


def remove_stop_words(text):
    
    # split the text to a list of words
    tokens = word_tokenize(text.lower())
    # setting the language
    stop_words = set(stopwords.words('english'))
    # remove stop words
    cleaned_text = [t for t in tokens if t not in stop_words]
    print(cleaned_text)
    print(type(cleaned_text))
    print(len(cleaned_text))
    for i in cleaned_text:
        print(i)
    return cleaned_text

def send_to_kafka(image: CleanedData):
        print(image.text)
        imageName = image.imageName
        #                           ! since its a class object, we need to convert it to dict and THEN to str
        image = json.dumps(image.__dict__).encode('utf-8')
        producer.produce(WRITING_TOPIC, image)
        logger.info(f"Sent image '{imageName}' to topic '{WRITING_TOPIC}'")
        producer.poll(0)



def clean():
    
    while True:
            image = consumer.poll(1.0) 
            if image is None: continue
            if image.error():
                print(f"cleaner error: {image.error()}")
                continue


            image = json.loads(image.value()) # from str to dict
            image = CleanedData(**image) # from dict to class object
            image.cleaned_text = re.sub(r"[?!-//)|:.,$#%@`]",'', image.text)

            image.cleaned_text = remove_stop_words(image.cleaned_text)
            send_to_kafka(image)
         
clean()

# python -m cleaning_consumer.main


