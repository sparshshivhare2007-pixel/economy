from telegram import Update
from telegram.ext import ContextTypes

async def items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows all available gift items with their prices."""
    msg = """📦 Available Gift Items:

🌹 Rose — $500
🍫 Chocolate — $800
💍 Ring — $2000
🧸 Teddy Bear — $1500
🍕 Pizza — $600
🎁 Surprise Box — $2500
🐶 Puppy — $3000
🎂 Cake — $1000
💌 Love Letter — $400
🐱 Cat — $2500
"""
    await update.message.reply_text(msg)
