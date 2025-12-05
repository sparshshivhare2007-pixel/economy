from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user, users  # <- database folder se import

async def sell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /sell item")

    item = context.args[0].lower()
    user = get_user(update.effective_user.id)

    prices = {"gun": 250, "shield": 150, "med": 100}

    if item not in prices:
        return await update.message.reply_text("❌ You don't have this item.")

    users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": prices[item]}})
    await update.message.reply_text(f"💰 You sold **{item}** for **${prices[item]}**!")
