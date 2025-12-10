# Copyright (c) 2025 Telegram:- @WTF_Phantom <DevixOP>
# Location: Supaul, Bihar 

# All rights reserved.
# This code is the intellectual property of @WTF_Phantom.

import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

# -------- ECONOMY BOT IMPORTS --------
from helpers.utils import ensure_user_exists, format_money
from database.main_db import user_db   # <-- your users collection


# ---------------------------------------------------
#                     DICE GAME
# ---------------------------------------------------

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Real Telegram Dice (Economy Bot Version)."""
    user = ensure_user_exists(update.effective_user)
    chat_id = update.effective_chat.id
    
    if not context.args:
        return await update.message.reply_text(
            "🎲 <b>Usage:</b> <code>/dice [amount]</code>", 
            parse_mode=ParseMode.HTML
        )
    
    try:
        bet = int(context.args[0])
    except:
        return await update.message.reply_text("⚠️ Invalid bet.", parse_mode=ParseMode.HTML)
    
    if bet < 50:
        return await update.message.reply_text("⚠️ Min bet is $50.", parse_mode=ParseMode.HTML)
    
    if user['balance'] < bet:
        return await update.message.reply_text("📉 Not enough money.", parse_mode=ParseMode.HTML)
    

    # Send the native Dice
    msg = await context.bot.send_dice(chat_id, emoji='🎲')
    result = msg.dice.value  # 1–6
    
    await asyncio.sleep(3)
    
    # WIN
    if result > 3:
        win_amt = bet
        user_db.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": win_amt}})
        
        return await update.message.reply_text(
            f"🎲 <b>Result:</b> {result}\n"
            f"🎉 <b>You Won!</b> +<code>{format_money(win_amt)}</code>",
            reply_to_message_id=msg.message_id,
            parse_mode=ParseMode.HTML
        )
    
    # LOSE
    user_db.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": -bet}})
    
    await update.message.reply_text(
        f"🎲 <b>Result:</b> {result}\n"
        f"💀 <b>You Lost!</b> -<code>{format_money(bet)}</code>",
        reply_to_message_id=msg.message_id,
        parse_mode=ParseMode.HTML
    )



# ---------------------------------------------------
#                     SLOT MACHINE
# ---------------------------------------------------

async def slots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Real Telegram Slot Machine (Economy Bot Version)."""
    user = ensure_user_exists(update.effective_user)
    chat_id = update.effective_chat.id
    
    bet = 100  # fixed bet
    
    if user["balance"] < bet:
        return await update.message.reply_text(
            "📉 Need $100 to spin.", 
            parse_mode=ParseMode.HTML
        )
    
    # Deduct bet
    user_db.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": -bet}})
    
    # Send native telegram slot dice
    msg = await context.bot.send_dice(chat_id, emoji='🎰')
    value = msg.dice.value
    
    await asyncio.sleep(2)
    
    # JACKPOT (777 → value=64)
    if value == 64:
        prize = bet * 10
        user_db.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": prize}})
        
        return await update.message.reply_text(
            f"🎰 <b>JACKPOT! (777)</b>\n"
            f"🎉 You won <code>{format_money(prize)}</code>!",
            reply_to_message_id=msg.message_id,
            parse_mode=ParseMode.HTML
        )

    # Normal fruit win (approximation values like 1,22,43)
    elif value in [1, 22, 43]:
        prize = bet * 3
        user_db.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": prize}})
        
        return await update.message.reply_text(
            f"🎰 <b>Winner!</b>\n"
            f"🎉 You won <code>{format_money(prize)}</code>!",
            reply_to_message_id=msg.message_id,
            parse_mode=ParseMode.HTML
        )

    # Lose
    await update.message.reply_text(
        "🎰 <b>Lost!</b> Better luck next time.",
        reply_to_message_id=msg.message_id,
        parse_mode=ParseMode.HTML
    )
