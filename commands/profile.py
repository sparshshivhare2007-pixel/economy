from telegram import Update
from telegram.ext import ContextTypes

# 🔥 Database import
from database.users import get_user


# ----------------- PROGRESS BAR -----------------
def make_progress_bar(current, total, length=10):
    """
    Creates a visual progress bar like:
    [██████░░░░]
    """
    if total == 0:
        return "[░░░░░░░░░░]"

    filled = int((current / total) * length)
    empty = length - filled
    return "█" * filled + "░" * empty


# ----------------- PROFILE -----------------
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    name = update.effective_user.first_name
    level = user.get("level", 1)
    xp = user.get("xp", 0)
    required_xp = level * 200  # Required XP per level

    progress = make_progress_bar(xp, required_xp)

    await update.message.reply_text(
        f"👤 <b>{name}'s Profile</b>\n\n"
        f"🏅 Badge: {user.get('badge', '🟢 Rookie')}\n"
        f"⭐ Level: {level}\n"
        f"📊 XP: [{progress}] {xp} / {required_xp}\n"
        f"💬 Messages: {user.get('messages_count', 0)}\n\n"
        f"💰 Balance: ${user.get('balance', 0)}\n"
        f"🏦 Bank: ${user.get('bank', 0)}\n"
        f"⚔️ Kills: {user.get('kills', 0)}\n"
        f"❤️ Status: {'☠️ Dead' if user.get('killed') else '🟢 Alive'}",
        parse_mode="HTML"
    )
