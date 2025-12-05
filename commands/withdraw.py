from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user, users  # database folder import

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /withdraw amount")

    try:
        amount = int(context.args[0])
    except ValueError:
        return await update.message.reply_text("❌ Invalid amount. Please provide a number.")

    user = get_user(update.effective_user.id)
    bank_amount = user.get("bank", 0)

    if bank_amount < amount:
        return await update.message.reply_text("❌ Not enough money in bank.")

    users.update_one(
        {"user_id": user["user_id"]},
        {"$inc": {"balance": amount, "bank": -amount}}
    )

    await update.message.reply_text(f"💸 Withdrawn **${amount}** from your bank!")
