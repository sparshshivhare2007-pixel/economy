# commands/kill.py
from random import randint
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from helpers.utils import resolve_target, format_money
from database.users import users, get_user

async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_obj = update.effective_user
    user = get_user(user_obj.id)
    target, error = await resolve_target(update, context)
    if not target or user["user_id"] == target["user_id"]:
        return await update.message.reply_text("⚠️ <b>Invalid target.</b>", parse_mode=ParseMode.HTML)
    target_doc = users.find_one({"user_id": target["user_id"]})
    if not target_doc:
        return await update.message.reply_text("⚠️ Target not found.", parse_mode=ParseMode.HTML)
    if target_doc.get("status") == "dead":
        return await update.message.reply_text("💀 Already dead.", parse_mode=ParseMode.HTML)
    if user.get("status") == "dead":
        return await update.message.reply_text("💀 Dead users cannot kill.", parse_mode=ParseMode.HTML)
    success = randint(1, 100)
    if success < 60:
        jail_fine = randint(100, 300)
        users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": -jail_fine}})
        return await update.message.reply_text(f"❌ <b>Attack Failed!</b>\n🚓 Police fined you <code>{format_money(jail_fine)}</code>", parse_mode=ParseMode.HTML)
    loot = target_doc.get("balance", 0) // 2
    users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": loot, "kills": 1}})
    users.update_one({"user_id": target_doc["user_id"]}, {"$set": {"status": "dead"}, "$inc": {"balance": -loot}})
    msg = (
        f"⚔️ <b>Kill Successful!</b>\n"
        f"💰 Looted: <code>{format_money(loot)}</code>\n"
        f"🔪 Total Kills: {user.get('kills', 0) + 1}"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
