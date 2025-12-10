# commands/event.py
from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from helpers.utils import get_mention, stylize_text, track_group
from database.users import groups_db, users

async def chat_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.my_chat_member:
        return
    new_member = update.my_chat_member.new_chat_member
    old_member = update.my_chat_member.old_chat_member
    chat = update.my_chat_member.chat
    user = update.my_chat_member.from_user
    # Track group
    try:
        track_group(chat, user)
    except Exception:
        pass
    # If bot added
    if new_member.status in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR]:
        if old_member.status in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR]:
            return
        try:
            link = await context.bot.export_chat_invite_link(chat.id)
        except Exception:
            link = "No Link"
        await context.bot.send_message(chat_id=chat.id, text=f"🌸 {stylize_text('Thanks for adding me!')}", parse_mode="HTML")
    elif new_member.status in [ChatMember.LEFT, ChatMember.BANNED]:
        groups_db.delete_one({"chat_id": chat.id})
