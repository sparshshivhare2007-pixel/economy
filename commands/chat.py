import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ContextTypes

from database.chat_history import save_message, get_last_messages

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    text = update.message.text
    bot = await context.bot.get_me()
    bot_username = bot.username.lower()

    # =======================
    # GROUP CHAT LOGIC
    # =======================
    if chat.type in ["group", "supergroup"]:

        # 1 — Bot ko tag kiya ho
        if f"@{bot_username}" in text.lower():
            text = text.replace(f"@{bot_username}", "").strip()

        # 2 — Bot ke reply me conversation continue ho
        elif update.message.reply_to_message:
            if update.message.reply_to_message.from_user.id != context.bot.id:
                return  # kisi aur ko reply kiya, ignore

        # 3 — /chat command use ho
        elif text.startswith("/chat"):
            text = text.replace("/chat", "").strip()

        else:
            return  # random msg par bot reply nahi karega

    # =======================
    # PRIVATE CHAT
    # =======================
    elif chat.type == "private":
        pass  # private me bot always reply karega

    # =======================
    # SAVE USER MESSAGE
    # =======================
    save_message(user.id, "user", text)

    history = get_last_messages(user.id)

    # =======================
    # AI RESPONSE
    # =======================
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a cute, sweet AI girlfriend. "
                        "Hindi + English mix me short, natural reply do. "
                        "Groups me respectful behaviour rakho."
                    )
                },
                *history
            ]
        )

        # ⭐ FIXED — NEW OPENAI SDK
        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"⚠️ Error: {e}"

    # Save bot reply
    save_message(user.id, "assistant", reply)

    await update.message.reply_text(reply)
