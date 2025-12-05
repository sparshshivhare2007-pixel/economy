from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user  # updated import for database folder

async def item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check your inventory items."""
    user = get_user(update.effective_user.id)

    if not user.get("items"):
        await update.message.reply_text(
            f"❛ {update.effective_user.first_name} has no items yet 😢"
        )
    else:
        item_list = "\n".join(user["items"])
        await update.message.reply_text(f"📦 Your Items:\n{item_list}")
