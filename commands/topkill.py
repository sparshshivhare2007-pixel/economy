from telegram import Update
from telegram.ext import ContextTypes
from database.users import users  # database folder se import

def make_clickable(user_id, name):
    safe = name if name else "Unknown User"
    return f"<a href='tg://user?id={user_id}'>{safe}</a>"

async def topkill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top_users = users.find().sort("kills", -1).limit(10)
    msg = "⚔️ <b>Top 10 Killers:</b>\n\n"

    for idx, user in enumerate(top_users, start=1):
        user_id = user["user_id"]
        kills = user.get("kills", 0)

        db_name = user.get("first_name") or user.get("name") or None

        try:
            chat = await context.bot.get_chat(user_id)
            if chat.username:
                name = f"@{chat.username}"
            else:
                name = make_clickable(user_id, chat.first_name or db_name)
        except:
            name = make_clickable(user_id, db_name)

        msg += f"{idx}. {name} — {kills} kills\n"

    await update.message.reply_text(msg, parse_mode="HTML")
