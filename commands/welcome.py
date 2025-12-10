from telegram import Update
from telegram.ext import ContextTypes
from helpers.utils import stylize_text, get_mention
from database.users import ensure_user_exists
from database.users import groups_db


async def welcome_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    member = update.message.new_chat_members[0]

    ensure_user_exists(member)

    text = (
        f"🎉 <b>{stylize_text('Welcome to the Group!')}</b>\n"
        f"{get_mention(member)}\n\n"
        f"🌸 Enjoy your stay!"
    )

    await update.message.reply_text(text, parse_mode="HTML")

    groups_db.update_one(
        {"group_id": chat.id},
        {"$set": {"last_welcome": member.id}},
        upsert=True
    )
