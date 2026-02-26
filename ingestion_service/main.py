from fastapi import FastAPI
import logging
from .connection.mongo import client
from .metadata import MetadataExtractor
from .text_extractor import TextExtractor
from .send.send_to_kafka import KafkaSender
from shared.logging_config import configure_logging

configure_logging("ingestion_service")



logging.getLogger("ingestion_service.kafka_sender")
logger = logging.getLogger(__name__)


db = client["week19"]
collection = db["images"]

app = FastAPI()

path = 'data\\messaging_images\\tweet_images'

metadata = MetadataExtractor()
text = TextExtractor()
kafka = KafkaSender()

# @app.get("/uploadfile")
# def get_file():
#     print('yo')
#     images = extract_metadata(path)
#     with_text =  get_clean_text(images)
#     return with_text

# @app.get("to_grid") # TODO: send to mongo
# def post_to_grid():
#     print("gotcha")
#     images = extract_metadata(path) # get the metadata
#     images = get_clean_text(images) # add the text
#     return kafka_send(images)

    
@app.post("/send_to_kafka")
def get_file():
    images = metadata.extract_metadata(path) # get the metadata
    for image in images:
        image_with_text = text.get_clean_text(image) # add the text
        kafka.send(image_with_text)
        # print(image_with_text.text)
    return {"count": len(images)}


    
# uvicorn ingestion_service.main:app --reload
