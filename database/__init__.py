# database/__init__.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB client
client = MongoClient(MONGO_URI)
db = client["economy_bot"]

# -------------------- COLLECTIONS --------------------
users_db = db["users"]       # Economy users
groups_db = db["groups"]     # Group tracking / status
couples_db = db["couples"]   # Couples for fun commands

# AI Chat Collections
chatai = db["chatai"]        # AI chat replies
chat_lang_db = db["ChatLangDb"]  # Chat language tracking
chatbot_status_db = db["chatbot_status_db"]  # Bot status per chat (enabled/disabled)

# -------------------- RUNTIME TRACKING --------------------
runtime_users = set()  # In-memory users currently active
runtime_groups = set() # In-memory groups currently active

# -------------------- USER HELPERS --------------------
async def get_user(user_id: int):
    """
    Fetch a user, create if not exists.
    """
    user = await users_db.find_one({"user_id": user_id})
    if not user:
        new_user = {
            "user_id": user_id,
            "balance": 0,
            "bank": 0,
            "kills": 0,
            "killed": False,
            "daily_cooldown": 0
        }
        await users_db.insert_one(new_user)
        return new_user
    return user

async def add_group_id(group_id: int):
    """
    Track group in database.
    """
    await groups_db.update_one({"group_id": group_id}, {"$set": {"group_id": group_id}}, upsert=True)

async def is_group_open(group_id: int):
    """
    Check if economy is open in a group.
    """
    group = await groups_db.find_one({"group_id": group_id})
    return group.get("status") == "open" if group else False

async def set_group_status(group_id: int, status: str):
    """
    Set a group's economy status (open/closed).
    """
    await groups_db.update_one({"group_id": group_id}, {"$set": {"status": status}}, upsert=True)
