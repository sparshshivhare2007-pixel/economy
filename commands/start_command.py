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

    safe_name = html.escape(user_name)
    clickable_name = f"<a href='tg://user?id={user_id}'>{safe_name}</a>"

    if chat.type in ["group", "supergroup"]:
        try:
            await context.bot.send_message(
                chat_id=chat.id,
                text=f"👋 𝙃𝙚𝙡𝙡𝙤 {clickable_name}!\n𝙏𝙝𝙖𝙣𝙠𝙨 𝙛𝙤𝙧 𝙪𝙨𝙞𝙣𝙜 𝙈𝙮𝙧𝙖 𝙞𝙣 𝙩𝙝𝙞𝙨 𝙜𝙧𝙤𝙪𝙥 💙\n\n𝙐𝙨𝙚 /help 𝙩𝙤 𝙨𝙚𝙚 𝙖𝙡𝙡 𝙘𝙤𝙢𝙢𝙖𝙣𝙙𝙨!",
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"⚠ Admin notify failed: {e}")
        return

    get_user(user.id)

    text = (
        "✧˚ · . 𝙎𝙃𝙄𝙕𝙐𝙆𝘼 : 𝙎𝙚𝙢𝙭𝙮 𝘾𝙝𝙖𝙩𝙗𝙤𝙩 · ˚✧\n"
        f"➜ — {clickable_name} (💞)\n\n"
        "💫 <b>𝙏𝙝𝙚 𝘼𝙀𝙎𝙏𝙃𝙀𝙏𝙄𝘾 𝘼𝙄-𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝙀𝘾𝙊𝙉𝙊𝙈𝙔</b> 💫\n\n"
        "✧ <b>𝙁𝙚𝙖𝙩𝙪𝙧𝙚𝙨:</b>\n"
        "◎ 𝙆𝙞𝙡𝙡, 𝙍𝙤𝙗, 𝙋𝙧𝙤𝙩𝙚𝙘𝙩\n"
        "◎ 𝙆𝙞𝙨𝙨, 𝘾𝙤𝙪𝙥𝙡𝙚\n"
        "◎ 𝘾𝙡𝙖𝙞𝙢, 𝙂𝙞𝙫𝙚, 𝘿𝙖𝙞𝙡𝙮\n"
        "◎ 𝙎𝙖𝙨𝙨𝙮 𝘾𝙝𝙖𝙩𝙗𝙤𝙩 🤭\n\n"
        "✧ <b>𝙉𝙚𝙚𝙙 𝙝𝙚𝙡𝙥?</b>\n"
        "𝘾𝙡𝙞𝙘𝙠 𝙩𝙝𝙚 𝙗𝙪𝙩𝙩𝙤𝙣𝙨 ⤵️"
    )

    keyboard = [
        [
            InlineKeyboardButton("🔍 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 🔍", url="https://t.me/shizuka_network"),
            InlineKeyboardButton("🔍 𝙎𝙐𝙋𝙋𝙊𝙍𝙏 🔍", url="https://t.me/+FcTsOElPLgNlZjk1")
        ],
        [
            InlineKeyboardButton("↪ 𝙏𝙖𝙥 𝙈𝙚 𝘽𝙖𝙗𝙚𝙨 .", callback_data="tap_babes")
        ],
        [
            InlineKeyboardButton("🔍 𝙃𝙀𝙇𝙋 & 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎", callback_data="help_menu"),
            InlineKeyboardButton("✔️ 𝙊𝙒𝙉𝙀𝙍 𝘽𝘼𝘽𝙐", url="https://t.me/Its_Profess0r")
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

    # ---- tap babes ----
    if data == "tap_babes":
        if query.message.caption != "😳 𝙆𝙮𝙖 𝙝𝙤𝙖 𝙖𝙥𝙠𝙤 𝘽𝙖𝙗𝙮 💋":
            await query.edit_message_caption(
                caption="😳 𝙆𝙮𝙖 𝙝𝙤𝙖 𝙖𝙥𝙠𝙤 𝘽𝙖𝙗𝙮 💋",
                reply_markup=None
            )
        return

    # ---- help menu ----
    if data == "help_menu":
        help_text = (
            "📘 <b>𝙈𝙮𝙧𝙖 𝙃𝙚𝙡𝙥 𝙈𝙚𝙣𝙪</b>\n\n"
            "🔹 /bal — 𝘾𝙝𝙚𝙘𝙠 𝙗𝙖𝙡𝙖𝙣𝙘𝙚\n"
            "🔹 /rob — 𝙍𝙤𝙗 𝙨𝙤𝙢𝙚𝙤𝙣𝙚\n"
            "🔹 /kill — 𝙆𝙞𝙡𝙡 𝙨𝙤𝙢𝙚𝙤𝙣𝙚\n"
            "🔹 /revive — 𝙍𝙚𝙫𝙞𝙫𝙚\n"
            "🔹 /give — 𝙂𝙞𝙛𝙩 𝙢𝙤𝙣𝙚𝙮\n"
            "🔹 /protect — 𝘽𝙪𝙮 𝙥𝙧𝙤𝙩𝙚𝙘𝙩𝙞𝙤𝙣\n"
            "🔹 /transfer — 𝙊𝙬𝙣𝙚𝙧 𝙊𝙣𝙡𝙮\n"
        )
        keyboard = [
            [
                InlineKeyboardButton("⬅️ 𝘽𝙖𝙘𝙠", callback_data="back_start")
            ]
        ]

        await query.edit_message_caption(
            caption=help_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return

    # ---- back button ----
    if data == "back_start":

        user = update.effective_user
        user_name = user.first_name or "Unknown"
        user_id = user.id

        safe_name = html.escape(user_name)
        clickable_name = f"<a href='tg://user?id={user_id}'>{safe_name}</a>"

        start_text = (
            "✧˚ · . 𝙎𝙃𝙄𝙕𝙐𝙆𝘼 : 𝙎𝙚𝙢𝙭𝙮 𝘾𝙝𝙖𝙩𝙗𝙤𝙩 · ˚✧\n"
            f"➜ — {clickable_name} (💞)\n\n"
            "💫 <b>𝙏𝙝𝙚 𝘼𝙀𝙎𝙏𝙃𝙀𝙏𝙄𝘾 𝘼𝙄-𝙋𝙊𝙒𝙀𝙍𝙀𝘿 𝙀𝘾𝙊𝙉𝙊𝙈𝙔</b> 💫\n\n"
            "✧ <b>𝙁𝙚𝙖𝙩𝙪𝙧𝙚𝙨:</b>\n"
            "◎ 𝙆𝙞𝙡𝙡, 𝙍𝙤𝙗, 𝙋𝙧𝙤𝙩𝙚𝙘𝙩\n"
            "◎ 𝙆𝙞𝙨𝙨, 𝘾𝙤𝙪𝙥𝙡𝙚\n"
            "◎ 𝘾𝙡𝙖𝙞𝙢, 𝙂𝙞𝙫𝙚, 𝘿𝙖𝙞𝙡𝙮\n"
            "◎ 𝙎𝙖𝙨𝙨𝙮 𝘾𝙝𝙖𝙩𝙗𝙤𝙩 🤭\n\n"
            "✧ <b>𝙉𝙚𝙚𝙙 𝙝𝙚𝙡𝙥?</b>\n"
            "𝘾𝙡𝙞𝙘𝙠 𝙩𝙝𝙚 𝙗𝙪𝙩𝙩𝙤𝙣𝙨 ⤵️"
        )

        keyboard = [
            [
                InlineKeyboardButton("🔍 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 🔍", url="https://t.me/shizuka_network"),
                InlineKeyboardButton("🔍 𝙎𝙐𝙋𝙋𝙊𝙍𝙏 🔍", url="https://t.me/+FcTsOElPLgNlZjk1")
            ],
            [
                InlineKeyboardButton("↪ 𝙏𝙖𝙥 𝙈𝙚 𝘽𝙖𝙗𝙚𝙨 .", callback_data="tap_babes")
            ],
            [
                InlineKeyboardButton("🔍 𝙃𝙀𝙇𝙋 & 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎", callback_data="help_menu"),
                InlineKeyboardButton("👑 𝙊𝙒𝙉𝙀𝙍 𝘽𝘼𝘽𝙐", url="https://t.me/Its_Profess0r")
            ]
        ]

        await query.edit_message_caption(
            caption=start_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
