# database/groups.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["economy_bot"]

groups_db = db["groups"]

def add_group_id(group_id: int):
    if not groups_db.find_one({"group_id": group_id}):
        groups_db.insert_one({"group_id": group_id, "economy_open": True})

def is_group_open(group_id: int) -> bool:
    group = groups_db.find_one({"group_id": group_id})
    return group.get("economy_open", True) if group else True

def set_group_status(group_id: int, status: bool):
    groups_db.update_one({"group_id": group_id}, {"$set": {"economy_open": status}}, upsert=True)
