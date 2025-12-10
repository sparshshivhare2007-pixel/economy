# commands/admin.py
import html
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram.error import Forbidden

from database.users import users, groups_db, sudoers
from helpers.utils import SUDO_USERS, get_mention, resolve_target, format_money, reload_sudoers

# simple keyboard helper
def get_kb(act, arg):
    return InlineKeyboardMarkup([[InlineKeyboardButton("✅ Yes", callback_data=f"cnf|{act}|{arg}"),
                                  InlineKeyboardButton("❌ No", callback_data="cnf|cancel|0")]])

async def addsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(os.getenv("OWNER_ID", "0")):
        return await update.message.reply_text("⛔ Not allowed.")
    target_arg = context.args[0] if context.args else None
    target, err = await resolve_target(update, context, specific_arg=target_arg)
    if not target:
        return await update.message.reply_text(err or "Usage: /addsudo <id|@username>")
    if target['user_id'] in SUDO_USERS:
        return await update.message.reply_text("⚠️ Already sudo.")
    await update.message.reply_text(f"Promote {get_mention(target)}?", reply_markup=get_kb("addsudo", str(target['user_id'])))

async def rmsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(os.getenv("OWNER_ID", "0")):
        return await update.message.reply_text("⛔ Not allowed.")
    target_arg = context.args[0] if context.args else None
    target, err = await resolve_target(update, context, specific_arg=target_arg)
    if not target:
        return await update.message.reply_text(err or "Usage: /rmsudo <id|@username>")
    if target['user_id'] not in SUDO_USERS:
        return await update.message.reply_text("⚠️ Not a sudoer.")
    await update.message.reply_text(f"Demote {get_mention(target)}?", reply_markup=get_kb("rmsudo", str(target['user_id'])))

async def confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.from_user.id not in SUDO_USERS:
        return await q.message.edit_text("❌ Not for you.", parse_mode=ParseMode.HTML)
    data = q.data.split("|")
    act = data[1]
    if act == "cancel":
        return await q.message.edit_text("❌ Cancelled.", parse_mode=ParseMode.HTML)

    if act == "addsudo":
        uid = int(data[2])
        sudoers.insert_one({"user_id": uid})
        reload_sudoers(db)  # expects a db or collection - adapt if needed
        await q.message.edit_text(f"✅ Promoted <code>{uid}</code>.", parse_mode=ParseMode.HTML)
    elif act == "rmsudo":
        uid = int(data[2])
        sudoers.delete_one({"user_id": uid})
        reload_sudoers(db)
        await q.message.edit_text(f"🗑 Demoted <code>{uid}</code>.", parse_mode=ParseMode.HTML)
