# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>
# Location: Supaul, Bihar 

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatType

from baka.plugins.chatbot import ask_mistral_raw
from baka.database import riddles_collection, users_collection
from baka.utils import format_money, ensure_user_exists, get_mention
from baka.config import RIDDLE_REWARD


# ------------------------------------------
#              /riddle command
# ------------------------------------------
async def riddle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat
    if chat.type == ChatType.PRIVATE:
        return await update.message.reply_text("❌ Group Only!", parse_mode=ParseMode.HTML)

    # If riddle already active
    if riddles_collection.find_one({"chat_id": chat.id}):
        return await update.message.reply_text(
            "⚠️ A riddle is already active! Try guessing it.",
            parse_mode=ParseMode.HTML
        )

    msg = await update.message.reply_text(
        "🧠 <b>Generating AI Riddle...</b>",
        parse_mode=ParseMode.HTML
    )

    # AI Prompt
    prompt = (
        "Generate a short, clever, difficult riddle.\n"
        "Format exactly:\n"
        "Riddle: [Question] | Answer: [OneWord]\n"
        "No extra text."
    )

    ai = await ask_mistral_raw(
        system_prompt="You are a Riddle Master.",
        user_input=prompt
    )

    if not ai or "|" not in ai:
        return await msg.edit_text("⚠️ AI Error. Try again.", parse_mode=ParseMode.HTML)

    try:
        question = ai.split("|")[0].replace("Riddle:", "").strip()
        answer = ai.split("|")[1].replace("Answer:", "").strip().lower()
    except:
        return await msg.edit_text("⚠️ AI parsing failed.", parse_mode=ParseMode.HTML)

    riddles_collection.insert_one({
        "chat_id": chat.id,
        "answer": answer
    })

    await msg.edit_text(
        f"🧩 <b>𝐀𝐈 𝐑𝐢𝐝𝐝𝐥𝐞 𝐂𝐡𝐚𝐥𝐥𝐞𝐧𝐠𝐞!</b>\n\n"
        f"<i>{question}</i>\n\n"
        f"💰 <b>Reward:</b> <code>{format_money(RIDDLE_REWARD)}</code>\n"
        f"👇 <i>Reply with your answer!</i>",
        parse_mode=ParseMode.HTML
    )


# ------------------------------------------
#     Auto-check answers in group chat
# ------------------------------------------
async def check_riddle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat = update.effective_chat
    text = update.message.text.strip().lower()

    active = riddles_collection.find_one({"chat_id": chat.id})
    if not active:
        return

    if text != active["answer"]:
        return

    # Winner found
    user = ensure_user_exists(update.effective_user)

    users_collection.update_one(
        {"user_id": user["user_id"]},
        {"$inc": {"balance": RIDDLE_REWARD}}
    )

    riddles_collection.delete_one({"chat_id": chat.id})

    await update.message.reply_text(
        f"🎉 <b>Correct Answer!</b>\n\n"
        f"👤 <b>Winner:</b> {get_mention(user)}\n"
        f"💰 <b>Prize:</b> <code>{format_money(RIDDLE_REWARD)}</code>\n"
        f"🔑 <b>Answer:</b> <i>{active['answer'].title()}</i>",
        parse_mode=ParseMode.HTML
    )
