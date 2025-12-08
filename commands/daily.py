from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user, users
from helpers import is_group_open, format_delta
import datetime

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # ❌ is_group_open async nahi hai → await HATAO
    if not is_group_open(chat_id):
        return await update.message.reply_text("❌ Economy abhi CLOSED hai bhai.")

    # async DB read
    user_data = await get_user(user_id)

    now = datetime.datetime.utcnow()
    last_daily = user_data.get("daily_cooldown")

    if last_daily:
        remaining = (last_daily + datetime.timedelta(hours=24)) - now
        if remaining.total_seconds() > 0:
            return await update.message.reply_text(
                f"⏳ Daily already claimed! Try after {format_delta(remaining)}"
            )

    daily_amount = 500

    # PyMongo = sync functions → NO await
    users.update_one({"user_id": user_id}, {"$inc": {"balance": daily_amount}})
    users.update_one({"user_id": user_id}, {"$set": {"daily_cooldown": now}})

    await update.message.reply_text(
        f"💰 You received {daily_amount} coins for today! ✅"
    )
