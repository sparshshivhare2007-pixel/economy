from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user, user_db
from main import LEVEL_COST

async def levelup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    level = user.get("user_level", 1)

    if level >= 10:
        return await update.message.reply_text("🎉 You already reached MAX LEVEL (10)!")

    cost = LEVEL_COST[level]

    if user["balance"] < cost:
        return await update.message.reply_text(
            f"❌ Not enough coins!\n"
            f"Need: {cost} coins\n"
            f"Your Balance: {user['balance']}"
        )

    # Deduct coins + increase level
    user_db.update_one(
        {"user_id": user["user_id"]},
        {"$inc": {"user_level": 1, "balance": -cost}}
    )

    await update.message.reply_text(
        f"🎉 <b>LEVEL UP!</b>\n"
        f"You are now Level <b>{level+1}</b> 🔥",
        parse_mode="HTML"
    )
