from telegram import Update
from telegram.ext import ContextTypes
import random
import time
from database.users import get_user  # updated import

# ----------------- COUPLE GIFs / VIDEOS -----------------
COUPLE_GIFS = [
    "https://files.catbox.moe/37kw89.mp4",
    "https://files.catbox.moe/xaqacb.mp4",
    "https://files.catbox.moe/p0et48.mp4"
]

# In-memory couples storage: key = (user1_id, user2_id), value = timestamp
couples = {}

def clean_expired_couples():
    now = time.time()
    expired = [pair for pair, ts in couples.items() if now - ts > 86400]  # 24h expiry
    for pair in expired:
        del couples[pair]

# ----------------- MAIN COUPLE COMMAND -----------------
async def couple(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clean_expired_couples()
    chat = update.effective_chat

    members = []
    try:
        admins = await context.bot.get_chat_administrators(chat.id)
        for admin in admins:
            if not admin.user.is_bot:
                members.append(admin.user)

        user = update.effective_user
        if user not in members and not user.is_bot:
            members.append(user)

    except Exception:
        await update.message.reply_text(
            "⚠️ Bot needs to be admin or cannot fetch members 😅"
        )
        return

    if len(members) < 2:
        await update.message.reply_text("Group me kam se kam 2 members hone chahiye 😅")
        return

    attempts = 0
    max_attempts = 50
    while attempts < max_attempts:
        user1, user2 = random.sample(members, 2)
        pair_key = tuple(sorted([user1.id, user2.id]))
        if pair_key not in couples:
            couples[pair_key] = time.time()
            break
        attempts += 1
    else:
        pair_key = random.choice(list(couples.keys()))
        user1 = next(u for u in members if u.id == pair_key[0])
        user2 = next(u for u in members if u.id == pair_key[1])
        couples[pair_key] = time.time()

    # Pick random MP4
    gif_url = random.choice(COUPLE_GIFS)

    # Caption with clickable IDs
    caption = (
        f"💑 𝑻𝒐𝒅𝒂𝒚'𝒔 𝒄𝒐𝒖𝒑𝒍𝒆 💑\n\n"
        f"<b><a href='tg://user?id={user1.id}'>{user1.first_name}</a></b> 💖 "
        f"<b><a href='tg://user?id={user2.id}'>{user2.first_name}</a></b>\n\n"
        f"Today's couple! 🔥"
    )

    await update.message.reply_animation(
        animation=gif_url,
        caption=caption,
        parse_mode="HTML"
    )
