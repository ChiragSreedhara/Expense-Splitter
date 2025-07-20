import os
from dotenv import load_dotenv
import pymysql

load_dotenv()  # loads .env file variables into environment

def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
