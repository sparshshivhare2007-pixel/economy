from telegram import Update
from telegram.ext import ContextTypes
import random
from database.users import get_user, users  # sync DB
from helpers import is_group_open, is_protected, format_delta


def tag(user):
    name = user.first_name.replace("<", "").replace(">", "")
    return f"<a href='tg://user?id={user.id}'>{name}</a>"


async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    msg = update.message
    robber = update.effective_user

    # ---------------- Check if economy is open ----------------
    if not is_group_open(chat_id):  # sync
        return await msg.reply_text("❌ Economy abhi CLOSED hai bhai.")

    # Must reply to someone
    if not msg.reply_to_message:
        return await msg.reply_text("Reply karke /rob karo!")

    target = msg.reply_to_message.from_user

    # Prevent robbing bot or self
    if target.id == context.bot.id:
        return await msg.reply_text("🤖 Bot ko rob nahi kar sakta bhai!")
    if robber.id == target.id:
        return await msg.reply_text("❌ Khud ko rob kar lega kya? 😂")

    # ---------------- Protection Check ----------------
    protected, remaining = is_protected(target.id)  # sync
    if protected:
        return await msg.reply_text(
            f"❌ User is protected! Remaining: {format_delta(remaining)}"
        )

    # ---------------- Fetch user data ----------------
    robber_data = get_user(robber.id)  # sync
    target_data = get_user(target.id)  # sync

    if target_data.get("killed", False):
        return await msg.reply_text(f"💀 {target.first_name} toh already mar chuka hai!")

    target_balance = target_data.get("balance", 0)
    if target_balance <= 0:
        return await msg.reply_text(
            f"😒 {target.first_name} ke paas kuch nahi hai lootne ko!"
        )

    # ---------------- Rob amount ----------------
    amount = random.randint(
        max(1, int(target_balance * 0.25)),
        max(1, int(target_balance * 0.45))
    )

    # ---------------- Update DB ----------------
    users.update_one({"user_id": robber.id}, {"$inc": {"balance": amount}})
    users.update_one({"user_id": target.id}, {"$inc": {"balance": -amount}})

    # ---------------- Reply in group ----------------
    robber_tag = tag(robber)
    target_tag = tag(target)

    await msg.reply_html(
        f"🤑 Rob Successful!\n"
        f"🔥 {robber_tag} ne {target_tag} ka {amount} coins loot liye! 😈"
    )

    # ---------------- DM notifications ----------------
    try:
        await context.bot.send_message(
            target.id,
            f"⚠️ Tumhe {robber_tag} ne rob kiya aur {amount} coins le gya!",
            parse_mode="HTML"
        )
    except Exception:
        pass

    try:
        await context.bot.send_message(
            robber.id,
            f"🎉 Tumne {target_tag} ko safalta se rob kar liya!",
            parse_mode="HTML"
        )
    except Exception:
        pass
