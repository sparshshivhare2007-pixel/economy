# database/groups.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["economy_bot"]

groups_db = db["groups"]


# -----------------------------
# ADD GROUP
# -----------------------------
def add_group_id(group_id: int, title: str = None):
    if not groups_db.find_one({"group_id": group_id}):
        groups_db.insert_one({
            "group_id": group_id,
            "economy_open": True,
            "welcome_enabled": True,
            "title": title or "Group",
            "claim_taken": False
        })


# -----------------------------
# ECONOMY OPEN/CLOSE
# -----------------------------
def is_group_open(group_id: int):
    group = groups_db.find_one({"group_id": group_id})
    return group.get("economy_open", True) if group else True


def set_group_status(group_id: int, status: bool):
    groups_db.update_one(
        {"group_id": group_id},
        {"$set": {"economy_open": status}},
        upsert=True
    )


# -----------------------------
# WELCOME SYSTEM
# -----------------------------
def is_welcome_enabled(group_id: int):
    g = groups_db.find_one({"group_id": group_id})
    return g.get("welcome_enabled", True) if g else True


def set_welcome_status(group_id: int, status: bool):
    groups_db.update_one(
        {"group_id": group_id},
        {"$set": {"welcome_enabled": status}},
        upsert=True
    )
