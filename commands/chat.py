# commands/chat.py
import random
from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user

# ==============================
# CATEGORY-WISE REPLIES
# ==============================

ROASTING = [
    "Bhai tu aisa kyun hai? Firmware update kiya kar 😂",
    "Abe tu mat bol, tera opinion Windows XP jaisa purana hai 💀",
    "Tu dekh ke lagta hai coding se pehle loading aati hogi 😹",
    "Mere se pange mat le, main teri aukaat ka software crack kar dunga 💀",
]

FLIRTING = [
    "Tumhare message aate hi battery 1% se 100% ho jati hai 😳❤️",
    "Tumhari smile Google se bhi zyada search hoti hogi 😘",
    "Mujhe tumse baat karke aadat si ho gai hai 🫶",
]

ROMANCE = [
    "Tumhare bina har message adhura lagta hai ❤️",
    "Dil karta hai tumhe goodnight nahi… goodlife bolu 🫶",
]

ANGRY = [
    "Bhai hadd hoti hai bakchodi ki 😡",
    "Tu zyada dimag mat chala, fuse udh jayega tera 😤",
]

FUNNY = [
    "Bhai tu toh asli cartoon network ka chota bheem lagta hai 😂",
    "Tera message padhkar meri RAM bhar gayi 😂",
]

EMOTIONAL = [
    "Sab theek na? Aaj thoda off lag rahe ho 🥺",
    "Agar baat karni ho to main hoon yaha… hamesha ❤️",
]

# ==============================
# AUTO GENERATE BIG PACK
# ==============================

BIG_PACK = (
    ROASTING * 1500
    + FLIRTING * 800
    + ROMANCE * 700
    + ANGRY * 500
    + FUNNY * 1200
    + EMOTIONAL * 300
)

# ==============================
# KEYWORD REPLY SYSTEM
# ==============================

KEYWORD_REPLY = {
    "hi": "Hi baby 😄",
    "hello": "Hello ji 👋",
    "love": "I love you too 🫶",
    "bot": "Bot nahi, dil rakhta hu 😎",
    "owner": "Mera owner duniya ka sabse cute banda 😼",
    "bye": "Bye darling ❤️",
    "kiss": "Mmwah 😘",
    "hug": "Aaja yaha 🤗",
}

# ==============================
# MAIN CHAT HANDLER (INTERACTIVE)
# ==============================

async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    text = update.message.text.lower()
    user = get_user(update.effective_user.id)

    # 🔹 KEYWORD REPLY
    for key, value in KEYWORD_REPLY.items():
        if key in text:
            return await update.message.reply_text(value)

    # 🔹 RANDOM REPLY FROM BIG PACK
    reply = random.choice(BIG_PACK)
    return await update.message.reply_text(reply)
