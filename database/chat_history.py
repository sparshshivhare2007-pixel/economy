from pymongo import MongoClient
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["chatbot_db"]

chat_history = db["chat_history"]

def save_message(user_id, role, content):
    chat_history.insert_one({
        "user_id": user_id,
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow()
    })

def get_last_messages(user_id, limit=10):
    messages = chat_history.find(
        {"user_id": user_id}
    ).sort("timestamp", -1).limit(limit)

    result = []
    for msg in reversed(list(messages)):
        result.append({"role": msg["role"], "content": msg["content"]})
    return result
