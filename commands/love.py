from telegram import Update
from telegram.ext import ContextTypes
import random

# 10 Love GIFs
LOVE_GIFS = [
    "https://media.giphy.com/media/3ohs4BSacFKI7A717y/giphy.gif",
    "https://media.giphy.com/media/l2JehQ2GitHGdVG9y/giphy.gif",
    "https://media.giphy.com/media/5ftsmLIqktHQA/giphy.gif",
    "https://media.giphy.com/media/xT9IgG50Fb7Mi0prBC/giphy.gif",
    "https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif",
    "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
    "https://media.giphy.com/media/l0MYEqEzwMWFCg8rm/giphy.gif",
    "https://media.giphy.com/media/3oEdv6n0B6cJk/giphy.gif",
    "https://media.giphy.com/media/l2QDM9Jnim1YVILXa/giphy.gif",
    "https://media.giphy.com/media/xT0xezQGU5xCDJuCPe/giphy.gif"
]

async def love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Lover (user sending command)
    lover = update.effective_user
    lover_name = lover.first_name
    lover_id = lover.id

    # Target user (reply required)
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
    elif context.args:
        await update.message.reply_text("Reply karke love meter check karo! 💕")
        return
    else:
        await update.message.reply_text("Kisko love meter me check karna hai? 💖 Reply karo!")
        return

    target_name = target.first_name
    target_id = target.id

    # Random compatibility percentage 0-100
    compatibility = random.randint(0, 100)

    # Random GIF
    gif_url = random.choice(LOVE_GIFS)

    # Caption with clickable IDs
    caption = (
        f"💕 Love meter report 💕\n\n"
        f"<b><a href='tg://user?id={lover_id}'>{lover_name}</a></b> 💖 "
        f"<b><a href='tg://user?id={target_id}'>{target_name}</a></b>\n\n"
        f"Love compatibility: {compatibility}% 🔥"
    )

    # Send GIF
    await update.message.reply_animation(
        animation=gif_url,
        caption=caption,
        parse_mode="HTML"
    )
