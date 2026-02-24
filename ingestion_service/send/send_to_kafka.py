from ..connection.kafka import producer
import os
import json
import logging
logger = logging.getLogger(__name__)


WRITING_TOPIC = os.getenv("INGESTION_WRITING_TOPIC", "RAW")


class KafkaSender:
    def send(self, image):
        try:#                            ! must when working with classes
            payload = json.dumps(image.__dict__).encode("utf-8")
            producer.produce(WRITING_TOPIC, payload)
            producer.poll(0)
            logger.info(f"Sent image '{image.imageName}' to topic '{WRITING_TOPIC}'")
        except Exception as e:
            raise
