# commands/rob.py
from random import randint
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from helpers.utils import resolve_target, format_money, stylize_text, get_mention
from database.users import users, get_user
from helpers.utils import ensure_user_exists  # if present in utils; else use get_user wrapper

# If ensure_user_exists not in helpers, use get_user directly.
try:
    ensure_user_exists
except NameError:
    def ensure_user_exists(u): return get_user(u.id)

async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_obj = update.effective_user
    user = get_user(user_obj.id)
    target, error = await resolve_target(update, context)
    if not target or user["user_id"] == target["user_id"]:
        return await update.message.reply_text("⚠️ <b>Invalid target.</b>", parse_mode=ParseMode.HTML)
    target_doc = users.find_one({"user_id": target["user_id"]})
    if target_doc is None:
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
        users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": -fine}})
        return await update.message.reply_text(f"❌ <b>Rob failed!</b>\nYou lost <code>{format_money(fine)}</code>", parse_mode=ParseMode.HTML)
    amount = randint(50, max(50, target_doc["balance"] // 2))
    users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": amount}})
    users.update_one({"user_id": target_doc["user_id"]}, {"$inc": {"balance": -amount}})
    msg = (
        f"🔫 <b>Successful Rob!</b>\n"
        f"💰 Stole: <code>{format_money(amount)}</code>\n\n"
        f"🏅 Good job!"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
