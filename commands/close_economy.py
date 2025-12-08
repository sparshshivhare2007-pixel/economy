from telegram import Update
from telegram.ext import ContextTypes
from database.groups import set_group_status  # updated import

async def close_economy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # ❌ Await mat lagayein agar async nahi hai
    set_group_status(chat_id, False)

    await update.message.reply_text("❌ Economy commands are now CLOSED in this group!")
