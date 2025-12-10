import datetime
from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user, users
from helpers.utils import stylize_text


async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    now = datetime.datetime.utcnow()
    last = user.get("daily_cooldown")

    if last:
        diff = (last + datetime.timedelta(hours=24)) - now
        if diff.total_seconds() > 0:
            return await update.message.reply_text(
                f"⏳ Already claimed!\n"
                f"Next in: <b>{int(diff.total_seconds()//3600)}h</b>",
                parse_mode="HTML"
            )

    amount = 500

    users.update_one(
        {"user_id": user_id},
        {"$set": {"daily_cooldown": now}, "$inc": {"balance": amount}}
    )

    await update.message.reply_text(
        f"💸 <b>{stylize_text('Daily Reward Claimed!')}</b>\n"
        f"You received <b>${amount}</b>.",
        parse_mode="HTML"
    )
