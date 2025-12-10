# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>

import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram.error import Forbidden

# Economy Bot DB
from database.users import get_all_users, delete_user
from database.groups import get_all_groups, delete_group

# Sudo User IDs
from config import SUDO_USERS


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast Manager — RyanBaka Style"""
    if update.effective_user.id not in SUDO_USERS:
        return
    
    args = context.args
    reply = update.message.reply_to_message

    # No Args + No Reply = Help Menu
    if not args and not reply:
        return await update.message.reply_text(
            "📢 <b>𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐌𝐚𝐧𝐚𝐠𝐞𝐫</b>\n\n"
            "<b>Usage:</b>\n"
            "‣ /broadcast -user (Reply to msg)\n"
            "‣ /broadcast -group (Reply to msg)\n\n"
            "<b>Flags:</b>\n"
            "‣ -clean : Copy msg (Use for Buttons/Media)\n",
            parse_mode=ParseMode.HTML
        )

    # Detect Target
    target_type = (
        "user" if "-user" in args else
        "group" if "-group" in args else None
    )

    if not target_type:
        return await update.message.reply_text(
            "⚠️ Missing flag: <code>-user</code> or <code>-group</code>",
            parse_mode=ParseMode.HTML
        )

    is_clean = "-clean" in args

    # Text broadcast (no reply message)
    msg_text = None
    if not reply:
        clean_args = [a for a in args if a not in ["-user", "-group", "-clean"]]
        if not clean_args:
            return await update.message.reply_text(
                "⚠️ Give me a message or reply to one.",
                parse_mode=ParseMode.HTML
            )
        msg_text = " ".join(clean_args)

    # Start Broadcast
    status_msg = await update.message.reply_text(
        f"⏳ <b>Broadcasting to {target_type}s...</b>",
        parse_mode=ParseMode.HTML
    )

    count = 0

    # Load Targets
    if target_type == "user":
        targets = get_all_users()
    else:
        targets = get_all_groups()

    # Loop Through Targets
    for doc in targets:
        cid = (
            doc.get("user_id")
            if target_type == "user"
            else doc.get("chat_id")
        )

        try:
            if reply:
                if is_clean:
                    await reply.copy(cid)  # Buttons / Media Safe
                else:
                    await reply.forward(cid)
            else:
                await context.bot.send_message(
                    chat_id=cid,
                    text=msg_text,
                    parse_mode=ParseMode.HTML
                )

            count += 1

            if count % 20 == 0:
                await asyncio.sleep(1)

        except Forbidden:
            # User/Group blocked or removed
            if target_type == "user":
                delete_user(cid)
            else:
                delete_group(cid)

        except Exception:
            pass

    # Final Report
    await status_msg.edit_text(
        f"✅ <b>Broadcast Complete!</b>\nSent to {count} {target_type}s.",
        parse_mode=ParseMode.HTML
    )
