# helpers/utils.py
import html
import asyncio
from typing import Tuple, Optional, Dict, Any
from telegram import Update
from telegram.ext import ContextTypes

# SUDO_USERS will be reloaded from DB
SUDO_USERS = []

def format_money(amount: int) -> str:
    try:
        return f"${int(amount)}"
    except Exception:
        return str(amount)

def get_mention(user_doc_or_dict: Dict[str, Any]) -> str:
    """
    Accepts either a MongoDB doc or a dict with keys 'user_id' and 'first_name'
    """
    try:
        uid = user_doc_or_dict.get("user_id")
        name = user_doc_or_dict.get("first_name") or user_doc_or_dict.get("name") or str(uid)
        return f"<a href='tg://user?id={uid}'><b>{html.escape(str(name))}</b></a>"
    except Exception:
        return "<b>User</b>"

async def resolve_target(update: Update, context: ContextTypes.DEFAULT_TYPE, specific_arg: Optional[str]=None) -> Tuple[Optional[Dict[str,Any]], Optional[str]]:
    """
    Try to resolve a target user from:
      - specific_arg numeric id or @username
      - reply_to_message
    Returns ({"user_id": id, "first_name": name}, None) or (None, "error message")
    """
    # 1) check reply
    if update.message and update.message.reply_to_message:
        u = update.message.reply_to_message.from_user
        return ({"user_id": u.id, "first_name": u.first_name}, None)

    # 2) specific arg (id/username)
    if specific_arg:
        # numeric id
        if specific_arg.isdigit():
            return ({"user_id": int(specific_arg), "first_name": specific_arg}, None)
        # @username
        if specific_arg.startswith("@"):
            try:
                chat = await context.bot.get_chat(specific_arg)
                return ({"user_id": chat.id, "first_name": getattr(chat, "first_name", specific_arg)}, None)
            except Exception as e:
                return (None, "User not found by username.")
    return (None, "No target found. Reply to a user or pass id/username.")

def reload_sudoers(mongo_db):
    """
    Load sudoers from mongo 'sudoers' collection and update global SUDO_USERS.
    Pass in a pymongo database object (db) or a collection object.
    """
    global SUDO_USERS
    SUDO_USERS = []
    try:
        sudo_col = None
        if hasattr(mongo_db, "sudoers"):
            sudo_col = mongo_db.sudoers
        else:
            sudo_col = mongo_db.get_collection("sudoers")
        for d in sudo_col.find():
            uid = d.get("user_id")
            if uid:
                SUDO_USERS.append(int(uid))
    except Exception:
        pass
    # ensure owner id included is external caller's responsibility
