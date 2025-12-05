from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user  # updated import
from database import users_db as users  # MongoDB collection
import random

async def farm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    # Earn random coins for farming
    earn = random.randint(30, 150)
    users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": earn}})

    await update.message.reply_text(f"🚜 You farmed crops and earned **${earn}**!", parse_mode="Markdown")
