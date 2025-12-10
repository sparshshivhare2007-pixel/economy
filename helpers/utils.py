# helpers/utils.py
import html
import random
import asyncio
from typing import Tuple, Optional, Dict, Any
from telegram import Update
from telegram.ext import ContextTypes

# SUDO_USERS will be reloaded from DB
SUDO_USERS = []

# ----------------------- RANDOM LOVE PERCENTAGE -----------------------
def random_percentage() -> int:
    """Returns a random 1–100 percentage."""
    return random.randint(1, 100)

# ----------------------- MONEY FORMATTER -----------------------
def format_money(amount: int) -> str:
    """Formats currency for economy commands."""
    try:
        return f"${int(amount)}"
    except Exception:
        return str(amount)

# ----------------------- MENTION BUILDER -----------------------
def get_mention(user_doc_or_dict: Dict[str, Any]) -> str:
    """
    Accepts MongoDB doc or dict with 'user_id' + 'first_name'
    """
    try:
        uid = user_doc_or_dict.get("user_id")
        name = (
            user_doc_or_dict.get("first_name")
            or user_doc_or_dict.get("name")
            or str(uid)
        )
        return f"<a href='tg://user?id={uid}'><b>{html.escape(str(name))}</b></a>"
    except Exception:
        return "<b>User</b>"

# ----------------------- TARGET RESOLVER -----------------------
async def resolve_target(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    specific_arg: Optional[str] = None
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Resolve a target user from:
      - reply_to_message
      - numeric id
      - @username
    Returns: (user_dict, None) OR (None, "error message")
    """

    # reply
    if update.message and update.message.reply_to_message:
        u = update.message.reply_to_message.from_user
        return ({"user_id": u.id, "first_name": u.first_name}, None)

    # argument
    if specific_arg:
        # numeric id
        if specific_arg.isdigit():
            return ({"user_id": int(specific_arg), "first_name": specific_arg}, None)

        # username
        if specific_arg.startswith("@"):
            try:
                chat = await context.bot.get_chat(specific_arg)
                return (
                    {"user_id": chat.id, "first_name": getattr(chat, "first_name", specific_arg)},
                    None
                )
            except Exception:
                return (None, "User not found by username.")

    return (None, "No target found. Reply to a user or pass id/username.")

# ----------------------- SUDOERS RELOADER -----------------------
def reload_sudoers(mongo_db):
    """
    Load sudoers from MongoDB collection 'sudoers'.
    Updates global SUDO_USERS list.
    """
    global SUDO_USERS
    SUDO_USERS = []
    try:
        sudo_col = (
            mongo_db.sudoers
            if hasattr(mongo_db, "sudoers")
            else mongo_db.get_collection("sudoers")
        )
        for d in sudo_col.find():
            uid = d.get("user_id")
            if uid:
                SUDO_USERS.append(int(uid))
    except Exception:
        pass
