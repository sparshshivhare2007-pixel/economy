# ---------------------------------------------------------
#       FINAL MERGED ECONOMY + RYAN BAKA USER DB
# ---------------------------------------------------------

from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["economy_bot"]

# ---------------------------------------------------------
# COLLECTIONS
# ---------------------------------------------------------
users = db["users"]             # full user profile
groups_db = db["groups"]        # group settings
sudoers = db["sudoers"]         # sudoers list
chatbot = db["chatbot"]         # AI chat memory
riddles = db["riddles"]         # riddles state

# ---------------------------------------------------------
#   CREATE / FETCH USER (FULL RYAN BAKA + ECONOMY STRUCTURE)
# ---------------------------------------------------------

def get_user(user_id: int, first_name: str = None):
    user = users.find_one({"user_id": user_id})

    if not user:
        user = {
            "user_id": user_id,
            "first_name": first_name or "User",

            # --- ECONOMY SYSTEM ---
            "balance": 0,
            "bank": 0,

            # --- XP SYSTEM ---
            "xp": 0,
            "level": 1,
            "badge": "🟢 Rookie",
            "messages_count": 0,

            # --- RYAN BAKA SYSTEM ---
            "inventory": [],
            "waifus": [],
            "kills": 0,
            "status": "alive",
            "death_time": None,
            "protection_until": None,
            "seen_groups": [],

            # timestamps
            "registered_at": datetime.utcnow(),
        }
        users.insert_one(user)

    return user


# RyanBaka Compatibility: used in waifu/shop/welcome system
def ensure_user_exists(user_obj):
    return get_user(user_obj.id, user_obj.first_name)


# ---------------------------------------------------------
# GROUP TRACKING (NEW FUNCTION ADDED TO FIX IMPORTERROR)
# ---------------------------------------------------------

def add_group_id(group_id: int):
    """
    Adds a group ID to the groups_db collection or updates its last_seen time.
    This tracks which groups the bot is active in.
    """
    groups_db.update_one(
        {"group_id": group_id},
        {"$set": {"last_seen": datetime.utcnow()}},
        upsert=True
    )

# ---------------------------------------------------------
# XP + LEVEL SYSTEM
# ---------------------------------------------------------

def add_message_count(user_id: int):
    user = get_user(user_id)

    new_xp = user.get("xp", 0) + 2
    msg_count = user.get("messages_count", 0) + 1

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
        {"$set": {
            "messages_count": msg_count,
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


# ---------------------------------------------------------
# PROTECTION SYSTEM
# ---------------------------------------------------------

def is_protected(user_id: int):
    user = get_user(user_id)
    until = user.get("protection_until")

    return bool(until and datetime.utcnow() < until)


# ---------------------------------------------------------
# TIME FORMATTER
# ---------------------------------------------------------

def format_delta(seconds: int):
    sec = int(seconds)
    h = sec // 3600
    sec %= 3600
    m = sec // 60
    s = sec % 60

    result = []
    if h: result.append(f"{h}h")
    if m: result.append(f"{m}m")
    if s or not result: result.append(f"{s}s")
    return " ".join(result)


# ---------------------------------------------------------
# EXPORT
# ---------------------------------------------------------

user_db = users
