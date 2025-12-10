# commands/chat.py
import os
from mistralai import Mistral
from telegram import Update
from telegram.ext import ContextTypes

from database.chat_history import save_message, get_last_messages
from helpers.config import MISTRAL_API_KEY

client = Mistral(api_key=MISTRAL_API_KEY)

async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    chat = message.chat
    user = message.from_user
    text = message.text or ""

    bot = await context.bot.get_me()
    bot_username = bot.username.lower()

    # GROUP triggers
    if chat.type in ["group", "supergroup"]:
        if f"@{bot_username}" in text.lower():
            text = text.replace(f"@{bot_username}", "").strip()
        elif message.reply_to_message:
            if message.reply_to_message.from_user.id != context.bot.id:
                return
        elif text.startswith("/chat"):
            text = text.replace("/chat", "").strip()
        else:
            return

    # PRIVATE
    elif chat.type == "private":
        pass

    # Save user message
    save_message(user.id, "user", text)
    history = get_last_messages(user.id, limit=10)

    chat_messages = [
        {
            "role": "system",
            "content": (
                "You are a cute, sweet AI girlfriend. Reply in short Hinglish (Hindi + English mix). "
                "Be natural, soft & emotional. In groups stay respectful."
            )
        }
    ]

    for h in history:
        chat_messages.append({"role": h["role"], "content": h["content"]})

    chat_messages.append({"role": "user", "content": text})

    # Mistral request
    try:
        output = client.chat.complete(
            model="mistral-small-latest",
            messages=chat_messages
        )

        # ✔ CORRECT WAY (using object attribute)
        reply = output.choices[0].message.content

    except Exception as e:
        reply = f"⚠️ AI Error: {e}"

    save_message(user.id, "assistant", reply)
    await message.reply_text(reply)
