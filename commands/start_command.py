from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from database.users import get_user
import html

BOT_IMAGE_URL = "https://files.catbox.moe/s0gtn8.jpg"


# ------------------- /start command -------------------
async def start_command(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user

    user_name = user.first_name or "Unknown"
    user_id = user.id

    # Safe clickable name
    safe_name = html.escape(user_name)
    clickable_name = f"<a href='tg://user?id={user_id}'>{safe_name}</a>"

    # --------- GROUP START ---------
    if chat.type in ["group", "supergroup"]:
        try:
            await context.bot.send_message(
                chat_id=chat.id,
                text=f"👋 Hello {clickable_name}!\nThanks for using Myra in this group 💙\n\nUse /help to see all commands!",
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"⚠ Admin notify failed: {e}")
        return

    # --------- DM START ---------
    get_user(user.id)  # Ensure user exists in DB

    # --------- START TEXT WITH AESTHETIC FONT ---------
    text = (
        "✧˚ · . 𝕊ℍ𝕀ℤ𝕌𝕂𝔸 : ꜱᴇᴍxʏ ᴄʜᴀᴛʙᴏᴛ · ˚✧\n"
        f"➜ — {clickable_name} (💞)\n\n"
        "💫 <b>The AESTHETIC AI-POWERED ECONOMY + RPG BOT!</b> 💫\n\n"
        "✧ <b>Features:</b>\n"
        "◎ ᴋɪʟʟ, ʀᴏʙ, ᴘʀᴏᴛᴇᴄᴛ\n"
        "◎ ᴋɪꜱꜱ, ᴄᴏᴜᴘʟᴇ\n"
        "◎ ᴄʟᴀɪᴍ, ɢɪᴠᴇ, ᴅᴀɪʟʏ\n"
        "◎ ꜱᴀꜱꜱʏ ᴄʜᴀᴛʙᴏᴛ 🤭\n\n"
        "✧ <b>Need help?</b>\n"
        "ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ⤵️"
    )

    keyboard = [
        [
            InlineKeyboardButton("☠️ SUPPORT ☠️", url="https://t.me/SELLING_HUBO"),
            InlineKeyboardButton("☠️ SUPPORT ☠️", url="https://t.me/SELLING_HUBO")
        ],
        [
            InlineKeyboardButton("↪ ᴛᴀᴘ ᴍᴇ ʙᴀʙᴇꜱ .", callback_data="tap_babes")
        ],
        [
            InlineKeyboardButton("❓ HELP & COMMANDS", callback_data="help_menu"),
            InlineKeyboardButton("✔️ OWNER BABU", url="https://t.me/sparsh_hu_yrr")
        ]
    ]

    await update.message.reply_photo(
        photo=BOT_IMAGE_URL,
        caption=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )


# ------------------- Callback query handler -------------------
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "tap_babes":
        await query.edit_message_caption(
            caption="😳 KYA HUA APKO BABY  💋",
            reply_markup=None
        )

    elif data == "help_menu":
        help_text = (
            "📘 <b>Myra Help Menu</b>\n\n"
            "🔹 /bal — Check balance\n"
            "🔹 /rob — Rob someone\n"
            "🔹 /kill — Kill someone\n"
            "🔹 /revive — Revive\n"
            "🔹 /give — Gift money\n"
            "🔹 /protect — Buy protection\n"
            "🔹 /transfer — Owner only\n"
        )
        keyboard = [
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_start")
            ]
        ]
        await query.edit_message_caption(
            caption=help_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )

    elif data == "back_start":
        # Use the same start command but simulate a DM call
        chat_id = query.message.chat_id
        # Create a dummy Update object for the DM context
        dummy_update = Update(update.update_id, message=query.message)
        await start_command(dummy_update, context)
