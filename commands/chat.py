# commands/chat.py
import os
import random
import asyncio
from typing import List, Dict, Any, Optional

import httpx
from telegram import Update
from telegram.ext import ContextTypes

# local DB helpers
from database.chat_history import save_message, get_last_messages
from database.users import get_user

# local utils (mention, formatting, etc.)
from helpers.utils import get_mention

# env
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
DEFAULT_MODEL = "mistral-small-latest"

# small fallback responses (Hinglish flavor)
FALLBACKS = [
    "Achha ji? 😊",
    "Hmm... aur batao?",
    "Okk okk! ✨",
    "Sahi hai yaar 💖",
    "Toh phir?",
    "Interesting! 🌸",
    "Aur kya chal raha?",
    "Sunao sunao! 💕",
    "Haan haan",
    "Theek hai 🥰"
]


async def _call_mistral_api(messages: List[Dict[str, Any]],
                            model: str = DEFAULT_MODEL,
                            timeout: int = 20) -> Optional[str]:
    """
    Call Mistral chat completions endpoint (simple wrapper).
    Returns assistant text on success or None on failure.
    """
    if not MISTRAL_API_KEY:
        return None

    payload = {
        "model": model,
        "messages": messages,
        # use moderate temperature to stay friendly
        "temperature": 0.7,
        "max_tokens": 512,
        "top_p": 0.9
    }

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.post(MISTRAL_URL, json=payload, headers=headers)
            if r.status_code != 200:
                return None
            data = r.json()
            # adapt to common "choices" structure if present
            # Try a few shapes for robustness
            if isinstance(data, dict):
                # model returns 'choices' -> [{ 'message': {'content': '...'} }]
                choices = data.get("choices")
                if choices and isinstance(choices, list):
                    first = choices[0]
                    # many APIs put assistant text in .message.content
                    if isinstance(first, dict):
                        msg = first.get("message") or first.get("text") or first.get("content")
                        if isinstance(msg, dict) and "content" in msg:
                            return msg["content"]
                        if isinstance(msg, str):
                            return msg
                    # sometimes direct 'text'
                    txt = first.get("text") or first.get("content")
                    if isinstance(txt, str):
                        return txt

                # or older shape: { "text": "..." }
                if "text" in data and isinstance(data["text"], str):
                    return data["text"]

            return None
    except Exception:
        return None


def _build_system_prompt() -> str:
    """
    The persona/system instructions for the assistant.
    Short and tuned for Hinglish girlfriend persona (non-explicit).
    """
    return (
        "You are a cute, sweet AI girlfriend. Reply in short Hinglish (mix of Hindi + English). "
        "Be natural, soft and emotional. Keep replies short (1-3 sentences). "
        "Avoid explicit / sexual / harmful content. In groups stay respectful and neutral."
    )


async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Main chat handler to plug into your Application:
      app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))
    Behaviour:
      - In private: always reply.
      - In group: reply if bot mentioned, or when replying to bot, or if '/chat' command used.
      - Saves user messages to chat history.
      - Tries Mistral API, otherwise falls back to canned replies.
    """
    msg = update.message
    if not msg or not msg.text:
        return

    chat = update.effective_chat
    user = update.effective_user

    text = msg.text.strip()
    if not text:
        return

    # Decide whether we should reply (PMs always)
    should_respond = False
    # If private chat -> always respond
    if chat.type == "private":
        should_respond = True
    else:
        # Group/supergroup triggers
        bot_username = (context.bot.username or "").lower()
        lower_text = text.lower()

        # 1) Reply to the bot's message
        if msg.reply_to_message and msg.reply_to_message.from_user and msg.reply_to_message.from_user.id == context.bot.id:
            should_respond = True

        # 2) Mention with @botusername
        elif bot_username and f"@{bot_username}" in lower_text:
            should_respond = True
            # remove mention for clarity when sending to model
            text = text.replace(f"@{bot_username}", "").strip()

        # 3) explicit /chat prefix (some users type it)
        elif lower_text.startswith("/chat"):
            should_respond = True
            text = text[len("/chat"):].strip()

        # 4) casual greeting triggers
        elif any(lower_text.startswith(k) for k in ("hey", "hi", "hello", "oye", "baka", "ai", "sun")):
            # respond only if bot is directly referenced or group has AI enabled (unknown here)
            # to avoid spam, only respond to greetings if bot is mentioned somewhere or it's a reply
            # we already checked reply and mention; so here we keep conservative behavior and do not auto-reply
            should_respond = False

    if not should_respond:
        return

    # Save message & retrieve recent history
    try:
        save_message(user.id, "user", text)
    except Exception:
        # non-fatal
        pass

    history = []
    try:
        history = get_last_messages(user.id, limit=10)
    except Exception:
        history = []

    # Build messages for model: system + history + current user
    messages = [{"role": "system", "content": _build_system_prompt()}]
    for h in history:
        # ensure role + content shape
        if "role" in h and "content" in h:
            messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": text})

    # Try Mistral (HTTP) first
    reply_text = None
    try:
        reply_text = await _call_mistral_api(messages)
    except Exception:
        reply_text = None

    # fallback simple heuristics if API fails
    if not reply_text:
        # quick local "Hinglish style" reply attempt
        # If user asked question (contains '?') give short friendly reply
        if "?" in text and len(text.split()) <= 10:
            reply_text = "Accha — acha. Main theek hoon! Tum batao? 😊"
        else:
            # random fallback
            reply_text = random.choice(FALLBACKS)

    # Save assistant reply
    try:
        save_message(user.id, "assistant", reply_text)
    except Exception:
        pass

    # Send reply (keep it simple plain text)
    try:
        await msg.reply_text(reply_text)
    except Exception:
        # If plain send fails, try simpler send
        try:
            await context.bot.send_message(chat_id=chat.id, text=reply_text)
        except Exception:
            # ultimate fallback: do nothing
            return
