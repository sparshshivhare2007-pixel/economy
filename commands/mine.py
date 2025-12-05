from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user, users
import random

async def mine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    earn = random.randint(50, 200)
    users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": earn}})
    await update.message.reply_text(f"⛏️ You mined and earned **${earn}**!")
