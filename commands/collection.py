from telegram import Update
from telegram.ext import ContextTypes
from helpers.utils import get_mention, stylize_text
from database.users import get_user, users


async def claim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.effective_user.id
    user = get_user(target)

    waifus = user.get("waifus", [])

    if context.args:
        name = " ".join(context.args)
        waifus.append(name)

        users.update_one(
            {"user_id": target},
            {"$set": {"waifus": waifus}}
        )

        return await update.message.reply_text(
            f"💘 {stylize_text('Waifu Claimed!')}\n"
            f"Added: <b>{name}</b>",
            parse_mode="HTML"
        )

    await update.message.reply_text(
        f"💞 <b>{stylize_text('Your Waifus')}</b>\n" +
        "\n".join(f"• {w}" for w in waifus) if waifus else "No waifus yet.",
        parse_mode="HTML"
    )
