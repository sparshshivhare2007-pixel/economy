# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>
# Location: Supaul, Bihar 

import os
import random
import asyncio
import io
import urllib.parse
from gtts import gTTS
from langdetect import detect
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatAction

# --- Your Economy DB ---
from database.users import get_user


# 🧩 Helper: mention format
def get_mention(user):
    return f"<a href='tg://user?id={user['user_id']}'>{user.get('first_name','User')}</a>"


# --- IMAGE SETTINGS ---
MODEL = "flux-anime"


# =======================================================
#                /draw  → Anime Image Maker
# =======================================================
async def draw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generates AI Images using Flux."""
    tg_user = update.effective_user
    user = get_user(tg_user.id, tg_user.first_name)

    if not context.args:
        return await update.message.reply_text(
            "🎨 <b>Usage:</b> <code>/draw a cute cat girl</code>", 
            parse_mode=ParseMode.HTML
        )

    user_prompt = " ".join(context.args)
    base_prompt = (
        f"{user_prompt}, anime style, masterpiece, best quality, "
        f"ultra detailed, 8k, vibrant colors, soft lighting"
    )
    encoded_prompt = urllib.parse.quote(base_prompt)

    msg = await update.message.reply_text("🎨 <b>Painting...</b>", parse_mode=ParseMode.HTML)

    try:
        seed = random.randint(0, 1000000)
        image_url = (
            f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            f"?width=1024&height=1024&seed={seed}&model={MODEL}&nologo=true"
        )

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=image_url,
            caption=(
                f"🖼️ <b>Art by Baka</b>\n"
                f"👤 {get_mention(user)}\n"
                f"✨ <i>{user_prompt}</i>"
            ),
            parse_mode=ParseMode.HTML
        )
        await msg.delete()

    except Exception as e:
        await msg.edit_text(
            f"❌ <b>Error:</b> Try again later.\n<code>{e}</code>",
            parse_mode=ParseMode.HTML
        )


# =======================================================
#                 TTS ENGINE  /speak
# =======================================================

def _generate_audio_sync(text):
    """Blocking function to be run in a separate thread."""
    try:
        lang_code = detect(text)
    except:
        lang_code = 'en'

    # Accent Logic
    if lang_code == 'hi' or any(x in text.lower() for x in ['kaise', 'kya', 'hai', 'nhi', 'haan', 'bol', 'sun']):
        selected_lang = 'hi'
        tld = 'co.in'
        voice_name = "Indian Girl"
    elif lang_code == 'ja':
        selected_lang = 'ja'
        tld = 'co.jp'
        voice_name = "Anime Girl"
    else:
        selected_lang = 'en'
        tld = 'us'
        voice_name = "English Girl"

    # Store audio in RAM
    audio_fp = io.BytesIO()
    tts = gTTS(text=text, lang=selected_lang, tld=tld, slow=False)
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)

    return audio_fp, voice_name


async def speak_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Smart Non-Blocking Text to Speech."""
    text = " ".join(context.args)

    if not text and update.message.reply_to_message:
        text = update.message.reply_to_message.text or update.message.reply_to_message.caption

    if not text:
        return await update.message.reply_text(
            "🗣️ <b>Usage:</b> <code>/speak Hello</code>", 
            parse_mode=ParseMode.HTML
        )

    if len(text) > 500:
        return await update.message.reply_text("❌ Text too long!", parse_mode=ParseMode.HTML)

    # Show mic indicator like RyanBaka
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, 
        action=ChatAction.RECORD_VOICE
    )

    try:
        loop = asyncio.get_running_loop()

        # Run TTS in thread so bot doesn't lag
        audio_bio, voice_name = await loop.run_in_executor(None, _generate_audio_sync, text)

        await context.bot.send_voice(
            chat_id=update.effective_chat.id,
            voice=audio_bio,
            caption=f"🗣️ <b>Voice:</b> {voice_name}\n📝 <i>{text[:50]}...</i>",
            parse_mode=ParseMode.HTML
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ <b>Audio Error:</b> <code>{e}</code>",
            parse_mode=ParseMode.HTML
        )
