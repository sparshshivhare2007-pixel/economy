from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user  # updated import
from database import users_db as users  # MongoDB collection

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /deposit <amount>")

    try:
        amount = int(context.args[0])
    except ValueError:
        return await update.message.reply_text("❌ Amount must be a number.")

    if amount <= 0:
        return await update.message.reply_text("❌ Amount must be greater than zero.")

    user = get_user(update.effective_user.id)

    if user.get("balance", 0) < amount:
        return await update.message.reply_text("❌ Not enough balance.")

    # --- Transfer balance to bank ---
    users.update_one(
        {"user_id": user["user_id"]},
        {"$inc": {"balance": -amount, "bank": amount}}
    )

    await update.message.reply_text(f"🏦 Deposited **${amount}** to your bank!", parse_mode="Markdown")
