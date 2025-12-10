import os
from mistralai import Mistral
from telegram import Update
from telegram.ext import ContextTypes

from database.chat_history import save_message, get_last_messages

# Load Mistral client
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    chat = message.chat
    user = message.from_user
    text = message.text or ""

    bot = await context.bot.get_me()
    bot_username = bot.username.lower()

    # =========================================================
    #                 GROUP CHAT MESSAGE TRIGGER
    # =========================================================
    if chat.type in ["group", "supergroup"]:

        # 1) Bot ko tag kiya ho
        if f"@{bot_username}" in text.lower():
            text = text.replace(f"@{bot_username}", "").strip()

        # 2) Bot ke reply me ho
        elif message.reply_to_message:
            if message.reply_to_message.from_user.id != context.bot.id:
                return

        # 3) /chat command
        elif text.startswith("/chat"):
            text = text.replace("/chat", "").strip()

        else:
            return  # random msgs ignore

    # ---------------------------------------------------------

    # PRIVATE chat always reply
    elif chat.type == "private":
        pass

    # =========================================================
    #               SAVE USER MESSAGE TO DATABASE
    # =========================================================
    save_message(user.id, "user", text)

    # Load last messages for context
    history = get_last_messages(user.id, limit=10)

    # Prepare history for Mistral
    chat_messages = [
        {
            "role": "system",
            "content": (
                "You are a cute sweet AI girlfriend. "
                "Reply in short Hinglish (Hindi + English mix). "
                "Be natural, soft, caring & emotional. "
                "In groups stay respectful and avoid adult content."
            )
        }
    ]

    for h in history:
        chat_messages.append({"role": h["role"], "content": h["content"]})

    # =========================================================
    #                   AI RESPONSE (MISTRAL)
    # =========================================================
    try:
        output = client.chat.complete(
            model="mistral-small-latest",
            messages=chat_messages
        )

        reply = output.choices[0].message["content"]

    except Exception as e:
        reply = f"⚠️ AI Error: {e}"

    # SAVE BOT RESPONSE
    save_message(user.id, "assistant", reply)

    # SEND MESSAGE
    await message.reply_text(reply)
