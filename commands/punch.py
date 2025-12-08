from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import random

# 10 Punch GIFs
PUNCH_GIFS = [
    "https://media.giphy.com/media/11rWoZNpAKw8w/giphy.gif",
    "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
    "https://media.giphy.com/media/l2JJKs3I69qfaQleE/giphy.gif",
    "https://media.giphy.com/media/3ohhwytHcusSCXXOUg/giphy.gif",
    "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
    "https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif",
    "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
    "https://media.giphy.com/media/l4FGuhL4U2WyjdkaY/giphy.gif",
    "https://media.giphy.com/media/26xBukh7hK6Kjqc4s/giphy.gif",
    "https://media.giphy.com/media/1rNW3uR9C5U9W/giphy.gif"
]

async def punch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Puncher (user sending command)
    puncher = update.effective_user
    puncher_name = puncher.first_name
    puncher_id = puncher.id

    # Target user (reply required)
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
    elif context.args:
        await update.message.reply_text("Reply karke punch karo! 👊")
        return
    else:
        await update.message.reply_text("Kisko punch karna hai? Reply karo! 😏")
        return

    target_name = target.first_name
    target_id = target.id

    # Random GIF
    gif_url = random.choice(PUNCH_GIFS)

    # Caption with clickable IDs
    caption = (
        f"<b><a href='tg://user?id={puncher_id}'>{puncher_name}</a></b> "
        f"punched "
        f"<b><a href='tg://user?id={target_id}'>{target_name}</a></b> 👊"
    )

    # Send GIF
    await update.message.reply_animation(
        animation=gif_url,
        caption=caption,
        parse_mode="HTML"
    )

# --------------------------
# Add this handler in main.py
# application.add_handler(CommandHandler("punch", punch))
