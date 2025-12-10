# commands/chat.py
import os
import random
import httpx
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatAction, ChatType

from helpers.utils import stylize_text, get_mention
from database.users import chatbot, users, get_user

# Load model keys from env (Mistral/Groq/Codestral if provided)
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CODESTRAL_API_KEY = os.getenv("CODESTRAL_API_KEY")

EMOJI_POOL = ["✨", "💖", "🌸", "😊", "🥰", "💕", "🎀", "🌺", "💫", "🦋"]

MODELS = {
    "mistral": {"url": "https://api.mistral.ai/v1/chat/completions", "model": "mistral-small-latest", "key": MISTRAL_API_KEY},
    "groq": {"url": "https://api.groq.com/openai/v1/chat/completions", "model": "llama3-70b-8192", "key": GROQ_API_KEY},
    "codestral": {"url": "https://codestral.mistral.ai/v1/chat/completions", "model": "codestral-latest", "key": CODESTRAL_API_KEY}
}

DEFAULT_MODEL = "mistral"
MAX_HISTORY = 8
FALLBACK_RESPONSES = ["Achha ji? 😊", "Hmm... aur batao?", "Okk okk! ✨", "Sahi hai yaar 💖"]

async def call_model_api(provider, messages, max_tokens=200):
    conf = MODELS.get(provider)
    if not conf or not conf.get("key"):
        return None
    headers = {"Authorization": f"Bearer {conf['key']}", "Content-Type": "application/json"}
    payload = {"model": conf["model"], "messages": messages, "temperature": 0.8, "max_tokens": max_tokens}
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(conf["url"], json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                # adapt for different providers
                if "choices" in data and data["choices"]:
                    # some providers return choice.message.content or choice.message["content"]
                    choice = data["choices"][0]
                    if isinstance(choice.get("message"), dict):
                        return choice["message"].get("content") or choice["message"].get("text")
                    return choice.get("text") or choice.get("message")
    except Exception as e:
        print("Model API error:", e)
    return None

async def get_ai_response(chat_id: int, user_input: str, user_name: str, selected_model=DEFAULT_MODEL):
    doc = chatbot.find_one({"chat_id": chat_id}) or {}
    history = doc.get("history", [])
    system_prompt = (
        "You are Baka, a sweet Indian girlfriend who replies conversationally in Hinglish. "
        "Stay respectful in groups. Keep replies short and natural."
    )
    messages = [{"role": "system", "content": system_prompt}]
    for m in history[-MAX_HISTORY:]:
        messages.append(m)
    messages.append({"role": "user", "content": user_input})

    # Try selected model
    reply = await call_model_api(selected_model, messages, max_tokens=200)
    if not reply and selected_model != "mistral":
        reply = await call_model_api("mistral", messages, max_tokens=200)
    if not reply:
        return random.choice(FALLBACK_RESPONSES), False

    # Cleanup and save
    reply = reply.replace("*", "").strip()
    new_history = history + [{"role": "user", "content": user_input}, {"role": "assistant", "content": reply}]
    if len(new_history) > MAX_HISTORY * 2:
        new_history = new_history[-(MAX_HISTORY * 2):]
    chatbot.update_one({"chat_id": chat_id}, {"$set": {"history": new_history}}, upsert=True)
    return reply, False

async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return
    chat = update.effective_chat
    user = update.effective_user
    text = msg.text.strip()

    # Group triggers
    if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        bot_username = context.bot.username.lower() if context.bot.username else ""
        if f"@{bot_username}" in text.lower():
            text = text.replace(f"@{bot_username}", "").strip()
        elif msg.reply_to_message and msg.reply_to_message.from_user.id == context.bot.id:
            pass
        elif text.startswith("/chat"):
            text = text.replace("/chat", "").strip()
        else:
            return

    # Save & respond
    chatbot.insert_one({"chat_id": chat.id, "user_id": user.id, "text": text, "ts": int(__import__("time").time())})
    await context.bot.send_chat_action(chat.id, ChatAction.TYPING)
    reply, is_code = await get_ai_response(chat.id, text, user.first_name, DEFAULT_MODEL)
    if is_code:
        await msg.reply_text(reply)
    else:
        await msg.reply_text(stylize_text(reply), parse_mode=ParseMode.HTML)
