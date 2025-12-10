# database/users.py
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["economy_bot"]

# Collections
users = db["users"]
groups_db = db["groups"]
sudoers = db["sudoers"]  # maintain list of sudoers

# Create/get user
def get_user(user_id: int):
    user = users.find_one({"user_id": user_id})
    if not user:
        user = {
            "user_id": user_id,
            "balance": 0,
            "bank": 0,
            "kills": 0,
            "killed": False,
            "protection_until": None,
            "messages_count": 0,
            "level": 1,
            "xp": 0,
            "badge": "🟢 Rookie"
        }
        users.insert_one(user)
    return user

# XP & message counter
def add_message_count(user_id: int):
    user = get_user(user_id)
    new_xp = user.get("xp", 0) + 2
    new_count = user.get("messages_count", 0) + 1
    level = user.get("level", 1)
    required = level * 200
    if new_xp >= required:
        level += 1
        new_xp = 0
        badge = get_badge(level)
    else:
        badge = user.get("badge", "🟢 Rookie")
    users.update_one(
        {"user_id": user_id},
        {"$set": {"messages_count": new_count, "xp": new_xp, "level": level, "badge": badge}}
    )

def get_badge(level: int):
    if level <= 3:
        return "🟢 Rookie"
    elif level <= 5:
        return "🔵 Skilled"
    elif level <= 7:
        return "🟣 Pro"
    elif level <= 10:
        return "🔥 Elite"
    elif level <= 15:
        return "👑 Master"
    else:
        return "💎 Legendary"

def is_protected(user_id: int):
    user = get_user(user_id)
    until = user.get("protection_until")
    if not until:
        return False
    return datetime.utcnow() < until

def format_delta(seconds: int):
    sec = int(seconds)
    h = sec // 3600
    sec %= 3600
    m = sec // 60
    s = sec % 60
    result = []
    if h > 0:
        result.append(f"{h}h")
    if m > 0:
        result.append(f"{m}m")
    if s > 0 or not result:
        result.append(f"{s}s")
    return " ".join(result)

# Group functions (sync)
def add_group_id(group_id: int):
    if not groups_db.find_one({"group_id": group_id}):
        groups_db.insert_one({"group_id": group_id, "economy_open": True})

def is_group_open(group_id: int):
    group = groups_db.find_one({"group_id": group_id})
    return group.get("economy_open", False) if group else False

def set_group_status(group_id: int, status: bool):
    groups_db.update_one({"group_id": group_id}, {"$set": {"economy_open": status}}, upsert=True)

# Expose user_db for ranking etc.
user_db = users
