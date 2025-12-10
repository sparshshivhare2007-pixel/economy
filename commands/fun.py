# commands/fun.py
import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from helpers.utils import random_percentage, get_mention, ensure_user_exists

async def hug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        await update.message.reply_text(f"🤗 {get_mention({'user_id': target.id, 'first_name': target.first_name})} got a hug!", parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text("🤗 Hug whom? Reply to someone.")

async def slap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        dmg = random.randint(1, 10)
        await update.message.reply_text(f"👊 {get_mention({'user_id': target.id, 'first_name': target.first_name})} got slapped! ({dmg} dmg)", parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text("👊 Reply to slap someone.")

async def crush(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
    elif context.args:
        return await update.message.reply_text("Reply to a user to check crush %.")
    else:
        target = update.effective_user
    pct = random_percentage()
    await update.message.reply_text(f"💘 {get_mention({'user_id': target.id, 'first_name': target.first_name})} crush chance: {pct}%", parse_mode=ParseMode.HTML)
