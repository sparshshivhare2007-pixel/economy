from telegram import Update
from telegram.ext import ContextTypes

# 🔥 Database import
from database.groups import set_group_status

# ----------------- OPEN ECONOMY -----------------
async def open_economy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # ✅ Await the DB update if async
    await set_group_status(chat_id, 1)  # 1 = OPEN

    await update.message.reply_text("✅ Economy commands are now OPEN in this group!")
