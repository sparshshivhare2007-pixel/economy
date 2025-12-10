from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# Economy Database
from database.users import get_user, users
from helpers.utils import format_money


async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    tg_user = update.effective_user

    user = get_user(user_id, tg_user.first_name)

    now = datetime.utcnow()
    last = user.get("last_daily")

    # -------------------------
    # DAILY COOLDOWN CHECK
    # -------------------------
    if last and (now - last) < timedelta(hours=24):
        rem = timedelta(hours=24) - (now - last)
        hours = rem.total_seconds() // 3600
        return await update.message.reply_text(
            f"⏳ <b>Cooldown!</b>\nCome back after <b>{int(hours)}h</b>.",
            parse_mode=ParseMode.HTML
        )

    # -------------------------
    # STREAK HANDLING
    # -------------------------
    streak = user.get("daily_streak", 0)

    # If user returns after 48h → streak reset
    if last and (now - last) > timedelta(hours=48):
        streak = 0

    streak += 1

    reward = 500
    bonus = 10000 if streak % 7 == 0 else 0

    # -------------------------
    # APPLY REWARD
    # -------------------------
    users.update_one(
        {"user_id": user_id},
        {
            "$set": {"last_daily": now, "daily_streak": streak},
            "$inc": {"balance": reward + bonus}
        }
    )

    # -------------------------
    # SEND MESSAGE
    # -------------------------
    msg = (
        f"📅 <b>Daily Reward — Day {streak}</b>\n"
        f"💰 Earned: <code>{format_money(reward)}</code>"
    )

    if bonus:
        msg += f"\n🎉 <b>Weekly Bonus:</b> <code>{format_money(bonus)}</code>"

    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
