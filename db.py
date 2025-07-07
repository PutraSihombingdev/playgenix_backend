import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    db_name = os.getenv("DB_NAME", "playgens")
    print("[DEBUG] DB yang dipakai:", db_name)
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=db_name
    )
