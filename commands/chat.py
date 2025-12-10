# commands/chat.py

import os
from mistralai import Mistral
from telegram import Update
from telegram.ext import ContextTypes

from database.chat_history import save_message, get_last_messages
from helpers.config import MISTRAL_API_KEY

# Correct Mistral client initialization
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

    # ============================
    # GROUP TRIGGERS
    # ============================
    if chat.type in ["group", "supergroup"]:

        # mention
        if f"@{bot_username}" in text.lower():
            text = text.replace(f"@{bot_username}", "").strip()

        # reply to bot
        elif message.reply_to_message:
            if message.reply_to_message.from_user.id != context.bot.id:
                return

        # /chat command
        elif text.startswith("/chat"):
            text = text.replace("/chat", "").strip()

        # else ignore
        else:
            return

    # PRIVATE: always respond
    elif chat.type == "private":
        pass

    # ============================
    # SAVE USER MESSAGE
    # ============================
    save_message(user.id, "user", text)

    history = get_last_messages(user.id, limit=10)

    messages_payload = [
        {
            "role": "system",
            "content": (
                "You are a cute, sweet AI girlfriend. Reply in short Hinglish (Hindi + English mix). "
                "Be natural, soft & emotional. In groups stay respectful and avoid adult/explicit content."
            )
        }
    ]

    for h in history:
        messages_payload.append({
            "role": h["role"],
            "content": h["content"]
        })

    messages_payload.append({"role": "user", "content": text})

    # ============================
    # AI RESPONSE
    # ============================
    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=messages_payload
        )

        # Mistral response format:
        # response.choices[0].message.content
        reply = response.choices[0].message["content"]

    except Exception as e:
        reply = f"⚠️ AI Error: {e}"

    # save bot reply
    save_message(user.id, "assistant", reply)

    # send reply
    await message.reply_text(reply)
