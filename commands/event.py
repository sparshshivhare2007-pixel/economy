# ============================================================
#   GROUP MANAGER — RyanBaka Style (Converted for Your Bot)
#   Works with: database/groups.py + helpers.py
# ============================================================

from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from database.groups import groups_db          # Your groups collection
from helpers import track_group, get_mention, log_to_channel


# ------------------------------------------------------------
# BOT STATUS HANDLER
# ------------------------------------------------------------
async def chat_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Bot added / removed / promoted / left handler
    Converted to match your economy bot structure.
    """
    data = update.my_chat_member
    if not data:
        return

    chat = data.chat
    user = data.from_user
    new = data.new_chat_member.status
    old = data.old_chat_member.status

    # Track group entry (your function)
    track_group(chat, user)

    # ------------------------------
    # BOT ADDED TO GROUP
    # ------------------------------
    if new in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR] and old not in [
        ChatMember.MEMBER,
        ChatMember.ADMINISTRATOR,
    ]:

        # Try fetching invite link if bot is admin
        invite_link = "No link (Bot not admin)"
        if new == ChatMember.ADMINISTRATOR:
            try:
                invite_link = await context.bot.export_chat_invite_link(chat.id)
            except:
                pass

        # Save group in DB
        groups_db.update_one(
            {"group_id": chat.id},
            {
                "$set": {
                    "title": chat.title,
                    "invite_link": invite_link,
                },
                "$inc": {"joined_count": 1},
            },
            upsert=True,
        )

        # Logging
        await log_to_channel(
            context.bot,
            "join",
            f"""
🟢 <b>Bot Added to Group</b>

👤 By: {get_mention(user)} (`{user.id}`)
🏷 Group: <b>{chat.title}</b> (`{chat.id}`)
🔗 Invite Link: {invite_link}
""",
        )

    # ------------------------------
    # BOT REMOVED / KICKED / LEFT
    # ------------------------------
    elif new in [ChatMember.LEFT, ChatMember.KICKED, ChatMember.BANNED]:
        groups_db.delete_one({"group_id": chat.id})

        await log_to_channel(
            context.bot,
            "leave",
            f"""
🔴 <b>Bot Removed from Group</b>

👤 By: {get_mention(user)} (`{user.id}`)
🏷 Group: <b>{chat.title}</b> (`{chat.id}`)
""",
        )


# ------------------------------------------------------------
# AUTO GROUP TRACKER ON EVERY MESSAGE
# ------------------------------------------------------------
async def group_tracker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Keep group updated (title, username, member count)
    Same style as RyanBaka but for your system.
    """
    chat = update.effective_chat
    user = update.effective_user

    if not chat or chat.type == "private":
        return

    track_group(chat, user)

    groups_db.update_one(
        {"group_id": chat.id},
        {
            "$set": {
                "title": chat.title,
            },
            "$inc": {"message_count": 1},
        },
        upsert=True,
    )
