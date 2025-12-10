# commands/game.py
import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from database.users import users
from helpers.utils import ensure_user_exists, format_money

async def coinflip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    if not context.args:
        return await update.message.reply_text("Usage: /coinflip <amount>")
    try:
        bet = int(context.args[0])
    except:
        return await update.message.reply_text("Enter valid number.")
    if user.get("balance",0) < bet:
        return await update.message.reply_text("Not enough balance.")
    await update.message.reply_text("Flipping coin...")
    await asyncio.sleep(1.2)
    res = random.choice(["heads","tails"])
    choice = "heads"  # default — we could allow user to choose
    if res == choice:
        users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": bet}})
        return await update.message.reply_text(f"You won! +{format_money(bet)}")
    else:
        users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": -bet}})
        return await update.message.reply_text(f"You lost! -{format_money(bet)}")
