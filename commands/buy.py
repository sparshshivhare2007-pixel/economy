from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user
from database import users_db as users

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /buy <item>")

    item = context.args[0].lower()
    user = get_user(update.effective_user.id)

    prices = {"gun": 500, "shield": 300, "med": 200}

    if item not in prices:
        return await update.message.reply_text("❌ Item not found.")

    price = prices[item]

    if user.get("balance", 0) < price:
        return await update.message.reply_text("❌ Not enough money.")

    users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": -price}})
    await update.message.reply_text(f"✅ You bought **{item}** for **${price}**!", parse_mode="Markdown")
