from telegram import Update
from telegram.ext import ContextTypes

# 🔥 Database imports
from database.users import get_user, users
from database.groups import is_group_open

# 🔥 Local helpers (no DB)
from helpers import is_protected, format_delta


async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # 1️⃣ Check if economy open (ASYNC!)
    if not await is_group_open(chat_id):
        return await update.message.reply_text(
            "❌ Economy commands abhi band hain is group me!"
        )

    msg = update.message

    # 2️⃣ Reply required
    if not msg.reply_to_message:
        return await msg.reply_text(
            "⚠️ Kisi ko kill karna hai? Uske message ka reply karo!"
        )

    killer = update.effective_user
    killer_id = killer.id

    target_user = msg.reply_to_message.from_user
    target_id = target_user.id

    BOT_ID = context.bot.id

    # 3️⃣ Don't allow killing bot
    if target_id == BOT_ID:
        return await msg.reply_text(
            "🤖 Bot ko kill? 😂\nBhai aukaat check kar… main immortal hoon!"
        )

    # 4️⃣ Prevent self-kill
    if killer_id == target_id:
        return await msg.reply_text(
            "❌ Apne aap ko kill? 😂\nBhai thoda calm ho ja!"
        )

    # 5️⃣ Protection check
    protected, remaining = is_protected(target_id)
    if protected:
        return await msg.reply_text(
            f"🛡️ {target_user.first_name} protected hai!\n"
            f"⏳ Remaining: {format_delta(remaining)}"
        )

    # 6️⃣ Check if already killed
    target_data = get_user(target_id)

    if target_data.get("killed", False):
        return await msg.reply_text(
            f"⚠️ {target_user.first_name} toh pehle hi swarg me VIP pass lekar baitha hai 😭\n"
            "Pehle revive karo fir bajana!"
        )

    # 7️⃣ Perform kill
    users.update_one({"user_id": killer_id}, {"$inc": {"kills": 1}})
    users.update_one({"user_id": target_id}, {"$set": {"balance": 0, "killed": True}})

    # 8️⃣ Success message
    return await msg.reply_text(
        f"⚔️ *Scene Over!*\n"
        f"🔥 {killer.first_name} ne {target_user.first_name} ko ek hi vaar me uda diya! 😈\n"
        f"💸 Balance → 0\n"
        f"💀 Status → KILLED\n"
        f"OP kill! 😎",
        parse_mode="Markdown"
    )
