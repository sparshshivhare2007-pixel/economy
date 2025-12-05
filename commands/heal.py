from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user  # updated import
from database import users_db as users  # MongoDB collection

async def heal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    if not user.get("killed", False):
        return await update.message.reply_text("❤️ You are already alive.")

    # Revive user
    users.update_one({"user_id": user["user_id"]}, {"$set": {"killed": False}})
    await update.message.reply_text("💖 You healed yourself and are alive again!")
