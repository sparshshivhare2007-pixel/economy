from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user, users  # ✅ database import

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)  # agar future me balance check karna ho
    await update.message.reply_text(
        "🛒 *Shop Items*\n"
        "• 🔫 Gun — $500\n"
        "• 🛡️ Shield — $300\n"
        "• 💊 Health Pack — $200\n\n"
        "Buy using: `/buy item_name`",
        parse_mode="Markdown"
    )
