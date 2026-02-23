from fastapi import FastAPI, File, UploadFile
import json
from connection.kafka import producer
from connection.mongo import client
from image import  extract_metadata
from text_extractor import get_clean_text

db = client["week19"]
collection = db["images"]

app = FastAPI()

path = 'data\\messaging_images\\tweet_images'

@app.get("/uploadfile")
def get_file():
    images = extract_metadata(path)
    with_text =  get_clean_text(images)
    return with_text

@app.post("to_grid")
def post_to_grid():
    images = extract_metadata(path) # get the metadata
    images = get_clean_text(images) # add the text


    











# uvicorn main:app --reload



    

