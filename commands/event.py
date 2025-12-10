# commands/events.py
import random
import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from database.users import users, groups_db
from helpers.utils import ensure_user_exists, format_money

# Simple "coin rain" event: admin triggers and gives small reward to random active users
async def coin_rain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(os.getenv("OWNER_ID", "0")):
        return await update.message.reply_text("⛔ Not authorized.")
    count = int(context.args[0]) if context.args and context.args[0].isdigit() else 5
    amt = int(context.args[1]) if len(context.args) > 1 and context.args[1].isdigit() else 50

    users_list = list(users.find({}))
    if not users_list:
        return await update.message.reply_text("No users found in DB.")
    winners = random.sample(users_list, min(count, len(users_list)))
    for w in winners:
        users.update_one({"user_id": w["user_id"]}, {"$inc": {"balance": amt}})
    txt = "🎉 Coin Rain!\n\n" + "\n".join([f"• <a href='tg://user?id={w['user_id']}'>{w.get('first_name','User')}</a> received {format_money(amt)}" for w in winners])
    await update.message.reply_text(txt, parse_mode=ParseMode.HTML)
