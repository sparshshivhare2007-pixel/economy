# economy_actions.py
from random import randint
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from baka.utils import ensure_user_exists, resolve_target, format_money, add_xp, get_user_badge, get_progress_bar
from baka.database import users_collection

async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    target, error = await resolve_target(update, context)
    if not target or user["user_id"] == target["user_id"]:
        return await update.message.reply_text("⚠️ <b>Invalid target.</b>", parse_mode=ParseMode.HTML)

    target_doc = users_collection.find_one({"user_id": target["user_id"]})
    if not target_doc:
        return await update.message.reply_text("⚠️ Target not found.", parse_mode=ParseMode.HTML)

    if target_doc.get("status") == "dead":
        return await update.message.reply_text("💀 You can't rob a dead person.", parse_mode=ParseMode.HTML)
    if user.get("status") == "dead":
        return await update.message.reply_text("💀 Dead people can't rob.", parse_mode=ParseMode.HTML)
    if target_doc.get("balance", 0) < 100:
        return await update.message.reply_text("🤣 Bro is broke.", parse_mode=ParseMode.HTML)

    success = randint(1, 100)
    if success < 40:
        fine = randint(50, 200)
        users_collection.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": -fine}})
        return await update.message.reply_text(f"❌ <b>Rob failed!</b>\nYou lost <code>{format_money(fine)}</code>", parse_mode=ParseMode.HTML)

    amount = randint(50, max(50, target_doc["balance"] // 2))
    users_collection.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": amount}})
    users_collection.update_one({"user_id": target_doc["user_id"]}, {"$inc": {"balance": -amount}})

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

async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = ensure_user_exists(update.effective_user)
    target, error = await resolve_target(update, context)
    if not target or user["user_id"] == target["user_id"]:
        return await update.message.reply_text("⚠️ <b>Invalid target.</b>", parse_mode=ParseMode.HTML)

    target_doc = users_collection.find_one({"user_id": target["user_id"]})
    if not target_doc:
        return await update.message.reply_text("⚠️ Target not found.", parse_mode=ParseMode.HTML)

    if target_doc.get("status") == "dead":
        return await update.message.reply_text("💀 Already dead.", parse_mode=ParseMode.HTML)
    if user.get("status") == "dead":
        return await update.message.reply_text("💀 Dead users cannot kill.", parse_mode=ParseMode.HTML)

    success = randint(1, 100)
    if success < 60:
        jail_fine = randint(100, 300)
        users_collection.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": -jail_fine}})
        return await update.message.reply_text(
            f"❌ <b>Attack Failed!</b>\n🚓 Police fined you <code>{format_money(jail_fine)}</code>",
            parse_mode=ParseMode.HTML
        )

    loot = target_doc.get("balance", 0) // 2
    users_collection.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": loot, "kills": 1}})
    users_collection.update_one({"user_id": target_doc["user_id"]}, {"$set": {"status": "dead"}, "$inc": {"balance": -loot}})

    leveled, level, xp = add_xp(user["user_id"], 30)
    next_xp = level * 200 if level < 5 else level * 500
    bar = get_progress_bar(xp, next_xp)
    badge = get_user_badge(level)

    msg = (
        f"⚔️ <b>Kill Successful!</b>\n"
        f"💰 Looted: <code>{format_money(loot)}</code>\n"
        f"🔪 Total Kills: {user.get('kills', 0) + 1}\n\n"
        f"🏅 XP: +30\n"
        f"🎮 Level: <b>{level}</b>\n"
        f"⭐ XP: <code>{xp} / {next_xp}</code>\n"
        f"{bar}\n"
        f"{badge}"
    )
    if leveled:
        msg += f"\n🎉 <b>LEVEL UP → {level}</b>"

    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
