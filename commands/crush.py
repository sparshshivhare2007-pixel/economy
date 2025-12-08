from telegram import Update
from telegram.ext import ContextTypes
from helpers.utils import random_percentage  # updated import

async def crush(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to someone to check your crush %.")

    target_user = update.message.reply_to_message.from_user
    target_name = target_user.first_name

    percent = random_percentage()

    await update.message.reply_text(f"💘 {target_name} Crush Percentage: {percent}%")
