# database/users.py
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["economy_bot"]

# Collections
users = db["users"]              # user stats, balance, xp
groups_db = db["groups"]         # group settings (welcome, economy toggle)
sudoers = db["sudoers"]          # admin permissions
chatbot = db["chatbot"]          # AI chat history
riddles = db["riddles"]          # active riddles

# -----------------------------
# USER CREATION / FETCH
# -----------------------------
def get_user(user_id: int, first_name: str = None):
    user = users.find_one({"user_id": user_id})

    if not user:
        user = {
            "user_id": user_id,
            "first_name": first_name or "User",
            "balance": 0,
            "bank": 0,
            "kills": 0,
            "killed": False,
            "protection_until": None,
            "messages_count": 0,
            "level": 1,
            "xp": 0,
            "badge": "🟢 Rookie",
            "inventory": [],
            "waifus": [],
            "status": "alive",
            "death_time": None
        }
        users.insert_one(user)

    return user


# RyanBaka compatibility function
def ensure_user_exists(user_obj):
    """Used by welcome system, shop, waifu."""
    return get_user(user_obj.id, user_obj.first_name)


# -----------------------------
# XP & MESSAGE COUNT
# -----------------------------
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
        badge = user.get("badge")

    users.update_one(
        {"user_id": user_id},
        {"$set": {
            "messages_count": new_count,
            "xp": new_xp,
            "level": level,
            "badge": badge
        }}
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
    return "💎 Legendary"


# -----------------------------
# PROTECTION SYSTEM
# -----------------------------
def is_protected(user_id: int):
    user = get_user(user_id)
    until = user.get("protection_until")
    return bool(until and datetime.utcnow() < until)


# -----------------------------
# TIME FORMATTER
# -----------------------------
def format_delta(seconds: int):
    sec = int(seconds)
    h = sec // 3600
    sec %= 3600
    m = sec // 60
    s = sec % 60

    res = []
    if h: res.append(f"{h}h")
    if m: res.append(f"{m}m")
    if s or not res: res.append(f"{s}s")
    return " ".join(res)


# -----------------------------
# EXPORT FOR RANKING
# -----------------------------
user_db = users
