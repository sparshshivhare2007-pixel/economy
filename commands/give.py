from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user  # updated import
from database import users_db as users  # MongoDB collection

async def give(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # --- Check if message is a reply ---
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to someone to give coins!")

    if len(context.args) == 0:
        return await update.message.reply_text("❌ Usage: /give <amount>")

    try:
        amount = int(context.args[0])
    except ValueError:
        return await update.message.reply_text("❌ Amount must be a number!")

    giver = get_user(update.effective_user.id)
    receiver_id = update.message.reply_to_message.from_user.id
    receiver = get_user(receiver_id)

    if giver.get("balance", 0) < amount:
        return await update.message.reply_text("❌ You don't have enough coins!")

    # --- Update balances ---
    users.update_one({"user_id": giver["user_id"]}, {"$inc": {"balance": -amount}})
    users.update_one({"user_id": receiver_id}, {"$inc": {"balance": amount}})

    await update.message.reply_text(
        f"💸 You sent **{amount} coins** to {receiver['user_id']}!", parse_mode="Markdown"
    )
