from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes, CommandHandler

# Warns store (in-memory)
user_warns = {}


# ------------------- Helper: Get Target User -------------------
def get_target(update: Update):
    if update.message.reply_to_message:
        return update.message.reply_to_message.from_user
    else:
        parts = update.message.text.split()
        if len(parts) >= 2 and parts[1].isdigit():
            return type("obj", (object,), {"id": int(parts[1]), "first_name": "User"})
    return None


# ------------------- BAN -------------------
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_target(update)
    chat = update.effective_chat
    bot = context.bot

    if not user:
        return await update.message.reply_text("⚠️ Reply or give user ID to ban.")

    try:
        await bot.ban_chat_member(chat.id, user.id)
        await update.message.reply_text(f"🚫 Banned: {user.first_name}")
    except:
        await update.message.reply_text("❌ I don't have permissions to ban.")


# ------------------- UNBAN -------------------
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_target(update)
    chat = update.effective_chat
    bot = context.bot

    if not user:
        return await update.message.reply_text("⚠️ Reply or give user ID to unban.")

    try:
        await bot.unban_chat_member(chat.id, user.id)
        await update.message.reply_text(f"♻️ Unbanned: {user.first_name}\nUser can rejoin now.")
    except:
        await update.message.reply_text("❌ Unable to unban user.")


# ------------------- MUTE -------------------
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_target(update)
    chat = update.effective_chat

    if not user:
        return await update.message.reply_text("⚠️ Reply or give user ID to mute.")

    try:
        await chat.restrict_member(
            user.id,
            ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text(f"🔇 Muted: {user.first_name}")
    except:
        await update.message.reply_text("❌ I don't have permission to mute.")


# ------------------- UNMUTE -------------------
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_target(update)
    chat = update.effective_chat

    if not user:
        return await update.message.reply_text("⚠️ Reply or give user ID to unmute.")

    try:
        await chat.restrict_member(
            user.id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await update.message.reply_text(f"🔊 Unmuted: {user.first_name}")
    except:
        await update.message.reply_text("❌ Unable to unmute user.")


# ------------------- WARN -------------------
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_target(update)
    if not user:
        return await update.message.reply_text("⚠️ Reply or give user ID to warn.")

    user_warns[user.id] = user_warns.get(user.id, 0) + 1
    warns = user_warns[user.id]

    await update.message.reply_text(
        f"⚠️ Warning issued to {user.first_name}\n"
        f"Total warns: {warns}"
    )


# ------------------- UNWARN -------------------
async def unwarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_target(update)

    if not user:
        return await update.message.reply_text("⚠️ Reply or give ID to unwarn.")

    if user.id not in user_warns or user_warns[user.id] == 0:
        return await update.message.reply_text("ℹ️ User has no warnings.")

    user_warns[user.id] -= 1
    await update.message.reply_text(
        f"♻️ Warning removed.\nRemaining warns: {user_warns[user.id]}"
    )


# ===================== REGISTER HANDLERS ========================
def register_group_management(app):
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("unban", unban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("warn", warn))
    app.add_handler(CommandHandler("unwarn", unwarn))
