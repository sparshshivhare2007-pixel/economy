from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import random

# 10 Slap GIFs
SLAP_GIFS = [
    "https://media.giphy.com/media/Gf3AUz3eBNbTW/giphy.gif",
    "https://media.giphy.com/media/jLeyZWgtwgr2U/giphy.gif",
    "https://media.giphy.com/media/mEtSQlxqBtWWA/giphy.gif",
    "https://media.giphy.com/media/Zau0yrl17uzdK/giphy.gif",
    "https://media.giphy.com/media/81kHQ5v9zbqzC/giphy.gif",
    "https://media.giphy.com/media/fO6UtDy5pWYwA/giphy.gif",
    "https://media.giphy.com/media/RXGNsyRb1hDJm/giphy.gif",
    "https://media.giphy.com/media/j3iGKfXRKlLqw/giphy.gif",
    "https://media.giphy.com/media/3XlEk2RxPS1m8/giphy.gif",
    "https://media.giphy.com/media/10Am8iduU0wO4/giphy.gif"
]

async def slap(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Slapper User
    slapper = update.effective_user
    slapper_name = slapper.first_name
    slapper_id = slapper.id

    # Target User (reply required)
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
    elif context.args:
        await update.message.reply_text("Reply karke slap karo taaki ID mil sake! 😏")
        return
    else:
        await update.message.reply_text("Kisko slap karna hai? Reply karo! 😎")
        return

    target_name = target.first_name
    target_id = target.id

    # Random GIF select
    gif_url = random.choice(SLAP_GIFS)

    # Caption with clickable IDs
    caption = (
        f"<b><a href='tg://user?id={slapper_id}'>{slapper_name}</a></b> "
        f"slapped "
        f"<b><a href='tg://user?id={target_id}'>{target_name}</a></b> 👋"
    )

    # Send GIF
    await update.message.reply_animation(
        animation=gif_url,
        caption=caption,
        parse_mode="HTML"
    )

# --------------------------
# Add this handler in main.py
# application.add_handler(CommandHandler("slap", slap))
