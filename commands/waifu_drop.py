# commands/waifu_drop.py

import random
import httpx
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# economy DB
from database.groups import groups_collection
from database.users import get_user, users_collection

# economy utils
from helpers.utils import get_mention

# In-Memory storage for drops
active_drops = {}

# Drop after every X messages
DROP_MESSAGE_COUNT = 100

WAIFU_NAMES = [
    ("Rem", "rem"), ("Ram", "ram"), ("Emilia", "emilia"), ("Asuna", "asuna"),
    ("Zero Two", "zero two"), ("Makima", "makima"), ("Nezuko", "nezuko"),
    ("Hinata", "hinata"), ("Sakura", "sakura"), ("Mikasa", "mikasa"),
    ("Yor", "yor"), ("Anya", "anya"), ("Power", "power")
]


# ------------------------#
#   AUTO DROP SYSTEM      #
# ------------------------#

async def check_drops(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Called on every message.
    Drops a waifu every DROP_MESSAGE_COUNT messages in a group.
    """
    msg = update.message
    chat = update.effective_chat

    if not msg or chat.type == "private":
        return

    # increase message counter
    group = groups_collection.find_one_and_update(
        {"chat_id": chat.id},
        {"$inc": {"msg_count": 1}},
        upsert=True,
        return_document=True
    )

    # if msg_count reached drop threshold
    if group.get("msg_count", 0) % DROP_MESSAGE_COUNT == 0:
        name, slug = random.choice(WAIFU_NAMES)

        # fetch waifu image
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(f"https://api.waifu.im/search?included_tags={slug}")
                url = (
                    r.json()["images"][0]["url"]
                    if r.status_code == 200
                    else "https://telegra.ph/file/5e5480760e412bd402e88.jpg"
                )
        except Exception:
            url = "https://telegra.ph/file/5e5480760e412bd402e88.jpg"

        # save active drop answer
        active_drops[chat.id] = name.lower()

        await msg.reply_photo(
            photo=url,
            caption=(
                "👧 <b>A Waifu Appeared!</b>\n\n"
                "Guess her name to collect her!\n"
                "<i>Reply to this image.</i>"
            ),
            parse_mode=ParseMode.HTML
        )


# ------------------------#
#   COLLECT WAIFU         #
# ------------------------#

async def collect_waifu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    User guesses waifu name → if correct, add to their collection.
    """
    msg = update.message
    chat = update.effective_chat

    if chat.id not in active_drops:
        return

    if not msg.text:
        return

    guess = msg.text.lower().strip()
    correct = active_drops[chat.id]

    if guess == correct:
        user = get_user(msg.from_user.id)
        del active_drops[chat.id]

        rarity = random.choice(["Common", "Rare", "Epic", "Legendary"])

        waifu_card = {
            "name": correct.title(),
            "rarity": rarity,
            "collected_at": datetime.utcnow()
        }

        # push into user DB
        users_collection.update_one(
            {"user_id": user["user_id"]},
            {"$push": {"waifus": waifu_card}}
        )

        await msg.reply_text(
            f"🎉 <b>Collected!</b>\n\n"
            f"👤 {get_mention(user)} caught <b>{correct.title()}</b>!\n"
            f"🌟 <b>Rarity:</b> {rarity}",
            parse_mode=ParseMode.HTML
        )
