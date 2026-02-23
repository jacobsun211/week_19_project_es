from ..connection.kafka import producer
import json

WRITING_TOPIC = "RAW"


def kafka_send(images):
    for image in images:
        image = json.dumps(image.model_dump()).encode('utf-8')
        producer.produce("RAW", image)
        producer.poll(0)  

    return {"count": len(images)}