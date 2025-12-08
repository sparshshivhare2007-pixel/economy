from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user

async def bank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    bank_amount = user.get("bank", 0)

    text = (
        "🏦 *Bank Account*\n"
        "💳 *Balance in bank:* "
        f"`$ {bank_amount}`"
    )

    await update.message.reply_text(
        text,
        parse_mode="MarkdownV2"
    )
