from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user  # updated import
from database import users_db as users  # MongoDB collection
from datetime import datetime

async def claim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    # --- Already claimed check ---
    if user.get("claimed"):
        return await update.message.reply_text("❌ You have already claimed your 3000 coins!")

    # --- Update balance + mark claimed ---
    users.update_one(
        {"user_id": user_id},
        {"$set": {"balance": 3000, "claimed": True}}
    )

    await update.message.reply_text("🎉 You claimed 3000 coins! 💰")
