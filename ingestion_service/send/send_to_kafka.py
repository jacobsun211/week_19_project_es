from connection.kafka import producer
import json


WRITING_TOPIC = "RAW"

class KafkaSender:

    def send(self, image):
        #                           ! since its a class object, we need to convert it to dict and THEN to str
        image = json.dumps(image.__dict__).encode('utf-8')
        producer.produce("RAW", image)
        producer.poll(0)

