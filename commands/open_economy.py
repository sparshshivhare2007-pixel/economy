from telegram import Update
from telegram.ext import ContextTypes
from database.groups import set_group_status  # sync version

async def open_economy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # NO await — sync DB
    set_group_status(chat_id, True)  # or 1 for open

    await update.message.reply_text("✅ Economy commands are now OPEN in this group!")
