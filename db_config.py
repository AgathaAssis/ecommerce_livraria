import os
from dotenv import load_dotenv
import mysql.connector  

load_dotenv()

def get_connection(database=None):
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=database or os.getenv("DB_NAME")
    )
