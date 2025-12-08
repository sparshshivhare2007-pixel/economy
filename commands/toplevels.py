from telegram import Update
from telegram.ext import ContextTypes
from database.users import user_db

async def toplevels(update: Update, context: ContextTypes.DEFAULT_TYPE):

    top = list(user_db.find().sort("user_level", -1).limit(20))

    text = "🌍 <b>GLOBAL LEVEL LEADERBOARD</b>\n\n"

    rank = 1
    for u in top:
        text += f"{rank}. 🏅 Level {u.get('user_level',1)} — <code>{u['user_id']}</code>\n"
        rank += 1

    await update.message.reply_text(text, parse_mode="HTML")
