# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>
# Location: Supaul, Bihar 
#
# All rights reserved.
#
# This code is the intellectual property of @WTF_Phantom.
# You are not allowed to copy, modify, redistribute, or use this
# code for commercial or personal projects without explicit permission.
#
# Allowed:
# - Forking for personal learning
# - Submitting improvements via pull requests
#
# Not Allowed:
# - Claiming this code as your own
# - Re-uploading without credit or permission
# - Selling or using commercially
#
# Contact for permissions:
# Email: king25258069@gmail.com

from datetime import datetime, timedelta
from random import randint
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from baka.utils import (
    ensure_user_exists, resolve_target, format_money,
    add_xp, get_user_badge, get_progress_bar
)
from baka.database import users_collection


# ------------------ DAILY COMMAND ------------------

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    now = datetime.utcnow()
    last = user.get("last_daily")
    
    if last and (now - last) < timedelta(hours=24):
        rem = timedelta(hours=24) - (now - last)
        return await update.message.reply_text(
            f"⏳ <b>Cooldown!</b> Wait {int(rem.total_seconds()//3600)}h.",
            parse_mode=ParseMode.HTML
        )
    
    streak = user.get("daily_streak", 0)
    if last and (now - last) > timedelta(hours=48):
        streak = 0  # Reset streak if late

    streak += 1
    reward = 500
    bonus = 10000 if streak % 7 == 0 else 0
    
    msg = (
        f"📅 <b>Day {streak}!</b>\n"
        f"Received: <code>{format_money(reward)}</code>"
    )
    if bonus:
        msg += f"\n🎉 <b>Weekly Bonus:</b> <code>{format_money(bonus)}</code>"
        
    users_collection.update_one(
        {"user_id": user['user_id']},
        {
            "$set": {"last_daily": now, "daily_streak": streak},
            "$inc": {"balance": reward + bonus}
        }
    )

    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)



# ------------------ ROB COMMAND ------------------

async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    target, error = await resolve_target(update, context)

    if not target or user["user_id"] == target["user_id"]:
        return await update.message.reply_text(
            "⚠️ <b>Invalid target.</b>", 
            parse_mode=ParseMode.HTML
        )

    if target["status"] == "dead":
        return await update.message.reply_text(
            "💀 You can't rob a dead person.", 
            parse_mode=ParseMode.HTML
        )

    if user["status"] == "dead":
        return await update.message.reply_text(
            "💀 Dead people can't rob.", 
            parse_mode=ParseMode.HTML
        )

    if target["balance"] < 100:
        return await update.message.reply_text(
            "🤣 Bro is broke.", 
            parse_mode=ParseMode.HTML
        )

    success = randint(1, 100)
    if success < 40:
        fine = randint(50, 200)
        users_collection.update_one(
            {"user_id": user["user_id"]}, {"$inc": {"balance": -fine}}
        )
        return await update.message.reply_text(
            f"❌ <b>Rob failed!</b>\n"
            f"You lost <code>{format_money(fine)}</code>",
            parse_mode=ParseMode.HTML
        )

    amount = randint(50, target["balance"] // 2)

    users_collection.update_one(
        {"user_id": user["user_id"]}, {"$inc": {"balance": amount}}
    )
    users_collection.update_one(
        {"user_id": target["user_id"]}, {"$inc": {"balance": -amount}}
    )

    # XP SYSTEM
    leveled, level, xp = add_xp(user["user_id"], 20)
    next_xp = level * 200 if level < 5 else level * 500
    bar = get_progress_bar(xp, next_xp)
    badge = get_user_badge(level)

    msg = (
        f"🔫 <b>Successful Rob!</b>\n"
        f"💰 Stole: <code>{format_money(amount)}</code>\n\n"
        f"🏅 XP: +20\n"
        f"🎮 Level: <b>{level}</b>\n"
        f"⭐ XP: <code>{xp} / {next_xp}</code>\n"
        f"{bar}\n"
        f"{badge}"
    )

    if leveled:
        msg += f"\n🎉 <b>LEVEL UP → {level}</b>"

    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)



# ------------------ KILL COMMAND ------------------

async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    target, error = await resolve_target(update, context)

    if not target or user["user_id"] == target["user_id"]:
        return await update.message.reply_text(
            "⚠️ <b>Invalid target.</b>", 
            parse_mode=ParseMode.HTML
        )

    if target["status"] == "dead":
        return await update.message.reply_text(
            "💀 Already dead.", 
            parse_mode=ParseMode.HTML
        )

    if user["status"] == "dead":
        return await update.message.reply_text(
            "💀 Dead users cannot kill.", 
            parse_mode=ParseMode.HTML
        )

    success = randint(1, 100)
    if success < 60:
        jail_fine = randint(100, 300)
        users_collection.update_one(
            {"user_id": user["user_id"]}, {"$inc": {"balance": -jail_fine}}
        )
        return await update.message.reply_text(
            f"❌ <b>Attack Failed!</b>\n"
            f"🚓 Police fined you <code>{format_money(jail_fine)}</code>",
            parse_mode=ParseMode.HTML
        )

    loot = target["balance"] // 2

    users_collection.update_one(
        {"user_id": user["user_id"]},
        {"$inc": {"balance": loot, "kills": 1}}
    )
    users_collection.update_one(
        {"user_id": target["user_id"]},
        {"$set": {"status": "dead"}, "$inc": {"balance": -loot}}
    )

    # XP SYSTEM
    leveled, level, xp = add_xp(user["user_id"], 30)
    next_xp = level * 200 if level < 5 else level * 500
    bar = get_progress_bar(xp, next_xp)
    badge = get_user_badge(level)

    msg = (
        f"⚔️ <b>Kill Successful!</b>\n"
        f"💰 Looted: <code>{format_money(loot)}</code>\n"
        f"🔪 Total Kills: {user['kills'] + 1}\n\n"
        f"🏅 XP: +30\n"
        f"🎮 Level: <b>{level}</b>\n"
        f"⭐ XP: <code>{xp} / {next_xp}</code>\n"
        f"{bar}\n"
        f"{badge}"
    )

    if leveled:
        msg += f"\n🎉 <b>LEVEL UP → {level}</b>"

    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
