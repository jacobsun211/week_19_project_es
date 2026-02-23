from fastapi import FastAPI
from connection.kafka import producer
from connection.mongo import client
from metadata import extract_metadata
from text_extractor import get_clean_text
from send.send_to_kafka import kafka_send

db = client["week19"]
collection = db["images"]

app = FastAPI()

path = 'data\\messaging_images\\tweet_images'

@app.get("/uploadfile")
def get_file():
    print('yo')
    images = extract_metadata(path)
    with_text =  get_clean_text(images)
    return with_text

@app.get("to_grid") # TODO: send to mongo
def post_to_grid():
    print("gotcha")
    images = extract_metadata(path) # get the metadata
    images = get_clean_text(images) # add the text
    return kafka_send(images)

    
@app.post("/bruhhh")
def get_file2():
    print("gotcha")
    images = extract_metadata(path) # get the metadata
    images = get_clean_text(images) # add the text
    return kafka_send(images)









# uvicorn main:app --reload



    

