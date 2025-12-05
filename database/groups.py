# database/groups.py
from . import groups_db  # import from database/__init__.py

async def is_group_open(chat_id: int) -> bool:
    """
    Check if a group has economy enabled/open.
    Defaults to True if not found.
    """
    group = await groups_db.find_one({"chat_id": chat_id})
    return group.get("open", True) if group else True

async def set_group_status(chat_id: int, status: bool):
    """
    Set the open/closed status of a group.
    """
    await groups_db.update_one(
        {"chat_id": chat_id},
        {"$set": {"open": status}},
        upsert=True
    )
