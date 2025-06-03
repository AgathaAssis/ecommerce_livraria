from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_mongo_client():
    return MongoClient(os.getenv("MONGO_URI"))

def get_mongo_db():
    client = get_mongo_client()
    return client[os.getenv("MONGO_DB_NAME")]
