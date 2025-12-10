import os
from mistralai import Mistral
from telegram import Update
from telegram.ext import ContextTypes

from database.chat_history import save_message, get_last_messages

# MISTRAL CLIENT
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    chat = msg.chat
    user = msg.from_user
    text = msg.text or ""

    bot = await context.bot.get_me()
    bot_username = bot.username.lower()

    # =====================================================
    #                 GROUP CHAT CONDITIONS
    # =====================================================
    if chat.type in ["group", "supergroup"]:

        # 1) Bot ko tag kiya gaya
        if f"@{bot_username}" in text.lower():
            text = text.replace(f"@{bot_username}", "").strip()

        # 2) Bot ke reply me ho
        elif msg.reply_to_message:
            if msg.reply_to_message.from_user.id != context.bot.id:
                return

        # 3) /chat command
        elif text.startswith("/chat"):
            text = text.replace("/chat", "").strip()

        else:
            return  # ignore normal messages

    # PRIVATE CHAT → ALWAYS REPLY
    elif chat.type == "private":
        pass

    # =====================================================
    #      SAVE USER MSG FOR HISTORY
    # =====================================================
    save_message(user.id, "user", text)
    history = get_last_messages(user.id)

    # Convert history to Mistral format
    chat_messages = [
        {
            "role": "system",
            "content": (
                "You are a cute sweet AI girlfriend. "
                "Hindi + English mix me natural aur short reply do. "
                "Group me respectful reply, no adult content."
            )
        }
    ]

    for h in history:
        chat_messages.append(
            {"role": h["role"], "content": h["content"]}
        )

    # =====================================================
    #                    AI RESPONSE
    # =====================================================
    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=chat_messages
        )

        reply = response.choices[0].message["content"]

    except Exception as e:
        reply = f"⚠️ AI Error: {e}"

    # SAVE BOT REPLY
    save_message(user.id, "assistant", reply)

    # SEND REPLY
    await msg.reply_text(reply)
