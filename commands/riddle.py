# commands/riddle.py
import random
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from database.users import users
from helpers.utils import format_money

RIDDLES = [
    ("I have keys but open no locks. What am I?", "keyboard"),
    ("What has hands but cannot clap?", "clock"),
    ("What has to be broken before you can use it?", "egg"),
]

active = {}  # chat_id -> answer

async def riddle_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    r = random.choice(RIDDLES)
    active[chat.id] = r[1].lower()
    await update.message.reply_text(f"🧩 Riddle: {r[0]}\nReply to this with your answer!")

async def riddle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.id not in active: return
    ans = active[chat.id]
    if update.message.text and update.message.text.lower().strip() == ans:
        uid = update.effective_user.id
        users.update_one({"user_id": uid}, {"$inc": {"balance": 200}}, upsert=True)
        del active[chat.id]
        await update.message.reply_text(f"✅ Correct! You earned {format_money(200)}.")
