# === FILE: database.py ===
from pymongo import MongoClient
import os
from lexie.config import MONGO_URI, MONGO_DB  # ✅ Update paths as needed

from dotenv import load_dotenv

load_dotenv()

# Read from .env
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "campus_connect")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# === Collections for Campus Connect ===
users_collection = db["users"]

# === Collections for Lexie AI ===
logs_collection = db.get_collection("logs")
feedback_collection = db.get_collection("feedback")
vector_data_collection = db.get_collection("vector_data")  # optional
