# =====================================================
#                    BROADCAST SYSTEM
# =====================================================
import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from helpers.utils import stylize_text
from database.users import users, groups_db
from config import OWNER_ID


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("⛔ You are not authorized.")

    msg = update.message
    sent = 0
    failed = 0

    # ------------------------------------------------
    # MODE 1: FORWARD BROADCAST
    # ------------------------------------------------
    if msg.reply_to_message:
        original = msg.reply_to_message
        await msg.reply_text("📣 Broadcast Started...")

        # Users
        for u in users.find():
            try:
                await original.forward(u["user_id"])
                sent += 1
                await asyncio.sleep(0.03)
            except:
                failed += 1

        # Groups
        for g in groups_db.find():
            try:
                await original.forward(g["group_id"])
                sent += 1
                await asyncio.sleep(0.03)
            except:
                failed += 1

        return await msg.reply_text(
            f"📢 <b>{stylize_text('Forward Broadcast Finished')}</b>\n"
            f"✅ Sent: {sent}\n❌ Failed: {failed}",
            parse_mode="HTML",
        )

    # ------------------------------------------------
    # MODE 2: TEXT BROADCAST
    # ------------------------------------------------
    if not context.args:
        return await msg.reply_text(
            "⚠️ Usage:\n"
            "/broadcast <message>\n"
            "Or reply to any message and run /broadcast"
        )

    text = " ".join(context.args)
    await msg.reply_text("📢 Sending message...")

    # Users
    for u in users.find():
        try:
            await context.bot.send_message(u["user_id"], text, parse_mode="HTML")
            sent += 1
            await asyncio.sleep(0.03)
        except:
            failed += 1

    # Groups
    for g in groups_db.find():
        try:
            await context.bot.send_message(g["group_id"], text, parse_mode="HTML")
            sent += 1
            await asyncio.sleep(0.03)
        except:
            failed += 1

    return await msg.reply_text(
        f"📢 <b>{stylize_text('Broadcast Complete')}</b>\n"
        f"✅ Sent: {sent}\n❌ Failed: {failed}",
        parse_mode="HTML",
    )
