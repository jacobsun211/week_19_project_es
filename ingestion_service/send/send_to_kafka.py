from connection.kafka import producer
import json

WRITING_TOPIC = "RAW"


def kafka_send(images):
    for image in images:
        print('before')
        print(image)
        print(type(image))
        image = json.dumps(image).encode('utf-8')
        print('afta')
        producer.produce("RAW", image)
        producer.poll(0)  

    return {"count": len(images)}