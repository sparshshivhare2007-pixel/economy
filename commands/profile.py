from telegram import Update
from telegram.ext import ContextTypes

# 🔥 Database import
from database.users import get_user

# ----------------- PROFILE -----------------
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    await update.message.reply_text(
        f"👤 Profile\n"
        f"💰 Balance: ${user.get('balance', 0)}\n"
        f"⚔️ Kills: {user.get('kills', 0)}\n"
        f"❤️ Status: {'Dead' if user.get('killed') else 'Alive'}"
    )
