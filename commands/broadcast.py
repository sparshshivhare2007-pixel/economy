from telegram import Update
from telegram.ext import ContextTypes
import asyncio
from database import runtime_users as users, runtime_groups as groups

OWNER_ID = 8379938997  # <-- apna ID

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        return await update.message.reply_text("⛔ Yeh command sirf owner ke liye reserved hai!")

    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /broadcast <message>")

    text = " ".join(context.args)
    sent = 0
    failed = 0

    for uid in users:
        try:
            await context.bot.send_message(uid, text)
            await asyncio.sleep(0.05)
            sent += 1
        except:
            failed += 1

    for gid in groups:
        try:
            await context.bot.send_message(gid, text)
            await asyncio.sleep(0.05)
            sent += 1
        except:
            failed += 1

    await update.message.reply_text(
        f"📢 **Broadcast Completed**\n\n✅ Sent: {sent}\n❌ Failed: {failed}",
        parse_mode="Markdown"
    )
