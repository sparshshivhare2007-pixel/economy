from telegram import Update
from telegram.ext import ContextTypes
from database.groups import set_group_status  # updated import

async def close_economy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # ✅ Await the DB update if async
    await set_group_status(chat_id, False)  # use False instead of 0

    await update.message.reply_text("❌ Economy commands are now CLOSED in this group!")
