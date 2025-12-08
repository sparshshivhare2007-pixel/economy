# database/groups.py

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)
db = client["economy_bot"]

groups_db = db["groups"]


async def is_group_open(chat_id: int) -> bool:
    """
    Check if a group's economy is open.
    Defaults to True if not found.
    """
    group = await groups_db.find_one({"chat_id": chat_id})
    return group.get("open", True) if group else True


async def set_group_status(chat_id: int, status: bool):
    """
    Set the economy open/close status for a group.
    """
    await groups_db.update_one(
        {"chat_id": chat_id},
        {"$set": {"open": status}},
        upsert=True
    )
