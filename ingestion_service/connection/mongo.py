import os
from pymongo import MongoClient


class MongoConnection:
    def __init__(self):
        host = os.getenv("MONGO_HOST", "localhost")
        port = int(os.getenv("MONGO_PORT", "27017"))

        MONGO_USER = os.getenv("MONGO_USER","app")          # e.g. "app"
        MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "app_pw")      # e.g. "app_pw"
        MONGO_AUTHSOURCE = os.getenv("MONGO_AUTHSOURCE", "admin")  # root user auth DB is typically admin [page:2]
        MONGO_DB = os.getenv("MONGO_DB", "pizza")

        self.client = MongoClient(
            host,
            port,
            username=MONGO_USER,
            password=MONGO_PASSWORD,
            authSource=MONGO_AUTHSOURCE,
        )


client = MongoConnection().client
