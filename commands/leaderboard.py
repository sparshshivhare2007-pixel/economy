# commands/leaderboard.py
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from database.users import user_db
from helpers.utils import get_mention

def stylize_text(text: str) -> str:
    # small local stylize for headings
    return "".join({"A":"ᴧ"}.get(c,c) for c in text)

async def toprich(update: Update, context: ContextTypes.DEFAULT_TYPE):
    docs = list(user_db.find().sort("balance",-1).limit(10))
    if not docs:
        return await update.message.reply_text("No users yet.")
    lines = []
    for i, d in enumerate(docs, start=1):
        name = d.get("first_name", str(d["user_id"]))
        bal = d.get("balance",0)
        lines.append(f"{i}. <a href='tg://user?id={d['user_id']}'>{html.escape(name)}</a> — ${bal:,}")
    await update.message.reply_text("<b>🏆 Top Rich</b>\n\n" + "\n".join(lines), parse_mode=ParseMode.HTML)
