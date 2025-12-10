# leaderboard.py
# © 2025 WTF_Phantom | XP Global Leaderboard

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

# ECONOMY BOT DATABASE
from database.main_db import user_db
from helpers.utils import stylize_text   # optional if needed
from database.main_db import get_badge   # your level → badge system


async def global_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Fetch Top 10 users by LEVEL then XP
    top = list(
        user_db.find()
        .sort([("level", -1), ("xp", -1)])   # Multi-sort
        .limit(10)
    )

    if not top:
        return await update.message.reply_text("No users found in database.")

    text = "🏆 <b>Global XP Leaderboard</b>\n"
    text += "━━━━━━━━━━━━━━━━━━\n"

    rank = 1
    for u in top:
        name = u.get("first_name", "User")
        level = u.get("level", 1)
        xp = u.get("xp", 0)

        # Badge using your economy bot badge system
        badge = get_badge(level)

        text += (
            f"<b>{rank}.</b> {badge} | <b>{name}</b>\n"
            f"  Lvl: <b>{level}</b> • XP: <code>{xp}</code>\n"
        )

        rank += 1

    text += "━━━━━━━━━━━━━━━━━━"

    await update.message.reply_text(text, parse_mode=ParseMode.HTML)
