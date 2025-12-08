# database/__init__.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Sync MongoDB client
client = MongoClient(MONGO_URI)
db = client["economy_bot"]

# Collections
users_db = db["users"]
groups_db = db["groups"]
couples_db = db["couples"]

chatai = db["chatai"]
chat_lang_db = db["ChatLangDb"]
chatbot_status_db = db["chatbot_status_db"]

runtime_users = set()
runtime_groups = set()

# -------- USERS --------
def get_user(user_id: int):
    user = users_db.find_one({"user_id": user_id})
    if not user:
        new_user = {
            "user_id": user_id,
            "balance": 0,
            "bank": 0,
            "kills": 0,
            "killed": False,
            "daily_cooldown": 0
        }
        users_db.insert_one(new_user)
        return new_user
    return user


# -------- GROUPS --------
def add_group_id(group_id: int):
    groups_db.update_one(
        {"group_id": group_id},
        {"$set": {"group_id": group_id}},
        upsert=True
    )

def is_group_open(group_id: int):
    group = groups_db.find_one({"group_id": group_id})
    return group.get("status") == "open" if group else False

def set_group_status(group_id: int, status: str):
    groups_db.update_one(
        {"group_id": group_id},
        {"$set": {"status": status}},
        upsert=True
    )
