# database/users.py
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# -------------------- LOAD ENV --------------------
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["economy_bot"]

# -------------------- COLLECTIONS --------------------
users = db["users"]       # Users collection (balance, kills, bank)
user_db = users            # Alias for compatibility with old imports
groups_db = db["groups"]   # Groups tracking for economy open/close

# -------------------- USER HELPERS --------------------
def get_user(user_id: int):
    """
    Fetch a user from DB. Create new if not exists.
    """
    user = users.find_one({"user_id": user_id})
    if not user:
        user = {
            "user_id": user_id,
            "balance": 0,
            "bank": 0,
            "kills": 0,
            "killed": False,
            "protection_until": None,
            "first_name": None
        }
        users.insert_one(user)
    return user

def is_protected(user_id: int):
    """
    Check if a user has active protection.
    Returns (True, remaining timedelta) if protected, else (False, None)
    """
    user = get_user(user_id)
    until = user.get("protection_until")
    if until:
        now = datetime.utcnow()
        remaining = until - now
        if remaining.total_seconds() > 0:
            return True, remaining
    return False, None

def format_delta(td: timedelta):
    """
    Format a timedelta object into a readable string like '1d 5h 20m'.
    """
    secs = int(td.total_seconds())
    days, rem = divmod(secs, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)
    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    return " ".join(parts) if parts else "0m"

# -------------------- GROUP HELPERS --------------------
def add_group_id(group_id: int):
    """
    Add a group to DB if not exists.
    """
    if not groups_db.find_one({"group_id": group_id}):
        groups_db.insert_one({"group_id": group_id, "economy_open": True})

def is_group_open(group_id: int):
    """
    Check if economy is open in a group. Defaults to False.
    """
    group = groups_db.find_one({"group_id": group_id})
    return group.get("economy_open", False) if group else False

def set_group_status(group_id: int, status: bool):
    """
    Set economy open/close status in a group.
    """
    groups_db.update_one(
        {"group_id": group_id},
        {"$set": {"economy_open": status}},
        upsert=True
    )
