from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user, user_db

async def rank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    msgs = user.get("messages_count", 0)
    level = user.get("user_level", 1)
    balance = user.get("balance", 0)

    await update.message.reply_text(
        f"🌟 <b>Your Rank</b>\n\n"
        f"🧍 User: <b>{update.effective_user.first_name}</b>\n"
        f"💬 Messages: <b>{msgs}</b>\n"
        f"⭐ Level: <b>{level}</b>\n"
        f"💰 Balance: <b>{balance}</b>",
        parse_mode="HTML"
    )
