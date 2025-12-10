# commands/fun.py
import asyncio
import random
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from helpers.utils import stylize_text, get_mention, format_money
from database.users import users, get_user

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    if not context.args:
        return await update.message.reply_text("🎲 <b>Usage:</b> <code>/dice [amount]</code>", parse_mode=ParseMode.HTML)
    try:
        bet = int(context.args[0])
    except:
        return await update.message.reply_text("⚠️ Invalid bet.", parse_mode=ParseMode.HTML)
    if bet < 50:
        return await update.message.reply_text("⚠️ Min bet is $50.", parse_mode=ParseMode.HTML)
    if user["balance"] < bet:
        return await update.message.reply_text("📉 Not enough money.", parse_mode=ParseMode.HTML)
    msg = await context.bot.send_dice(update.effective_chat.id, emoji='🎲')
    await asyncio.sleep(3)
    result = msg.dice.value
    if result > 3:
        win_amt = bet
        users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": win_amt}})
        await update.message.reply_text(f"🎲 <b>Result:</b> {result}\n🎉 <b>You Won!</b> +<code>{format_money(win_amt)}</code>", parse_mode=ParseMode.HTML)
    else:
        users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": -bet}})
        await update.message.reply_text(f"🎲 <b>Result:</b> {result}\n💀 <b>You Lost!</b> -<code>{format_money(bet)}</code>", parse_mode=ParseMode.HTML)

async def slots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    bet = 100
    if user["balance"] < bet:
        return await update.message.reply_text("📉 Need $100 to spin.", parse_mode=ParseMode.HTML)
    users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": -bet}})
    msg = await context.bot.send_dice(update.effective_chat.id, emoji='🎰')
    await asyncio.sleep(2)
    value = msg.dice.value
    if value == 64:
        prize = bet * 10
        users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": prize}})
        text = f"🎰 <b>JACKPOT! (777)</b>\n🎉 You won <code>{format_money(prize)}</code>!"
    elif value in [1, 22, 43]:
        prize = bet * 3
        users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": prize}})
        text = f"🎰 <b>Winner!</b>\n🎉 You won <code>{format_money(prize)}</code>!"
    else:
        text = f"🎰 <b>Lost!</b> Better luck next time."
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)
