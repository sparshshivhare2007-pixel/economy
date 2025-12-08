from telegram import Update
from telegram.ext import ContextTypes
from database.users import get_user, users  # ✅ Database import
from datetime import datetime, timedelta
import re

# ---------------- HELPERS ----------------
def parse_duration(s: str):
    m = re.match(r"^(\d+)([dh])$", s.lower().strip())
    if not m:
        return None
    value, unit = m.groups()
    value = int(value)
    if unit == "d":
        return timedelta(days=value)
    if unit == "h":
        return timedelta(hours=value)
    return None

def format_delta(td: timedelta):
    secs = int(td.total_seconds())
    days, rem = divmod(secs, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)
    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    return " ".join(parts) if parts else "0m"

# ---------------- COMMAND ----------------
async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /protect 1d  (or 2d, 12h etc.)")

    duration_str = context.args[0]
    delta = parse_duration(duration_str)
    if not delta:
        return await update.message.reply_text(
            "Invalid duration. Use formats like `1d`, `2d`, `12h`.",
            parse_mode="Markdown"
        )

    user_id = update.effective_user.id
    user = get_user(user_id)
    now = datetime.utcnow()
    protection_until = now + delta

    users.update_one(
        {"user_id": user_id},
        {"$set": {"protection_until": protection_until}}
    )

    await update.message.reply_text(f"🛡️ You are now protected for {duration_str}.")
