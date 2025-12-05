from telegram import Update
from telegram.ext import CallbackContext

async def help_command(update: Update, context: CallbackContext):
    """Sends a complete guide of all bot commands including secret ones."""
    
    help_text = (
        "📜 *myra Bot Commands Guide*\n\n"

        "💰 *Economy Commands:*\n"
        "/balance - Check your balance or reply to see others\n"
        "/work - Work to earn coins\n"
        "/transfer amount - Owner only: Add/remove coins\n"
        "/claim - Claim daily reward\n"
        "/own - Owner only command\n"
        "/crush - Interact with a user\n"
        "/love - Interact with a user\n"
        "/slap - Slap a user\n"
        "/items - Show your items\n"
        "/item - Check a specific item\n"
        "/give amount - Gift coins to a user\n"
        "/daily - Claim daily coins\n"
        "/rob amount - Rob a user\n"
        "/protect 1d|2d - Buy protection\n"
        "/toprich - Top 10 richest users\n"
        "/topkill - Top 10 killers\n"
        "/kill - Kill a user\n"
        "/revive - Revive yourself or a friend\n"
        "/open - Open economy commands\n"
        "/close - Close economy commands\n\n"

        "🎮 *Fun Commands:*\n"
        "/punch - Punch a user\n"
        "/hug - Hug a user\n"
        "/couple - Couple interaction\n\n"

        "🕵️ *Hidden Secret Economy Commands:*\n"
        "/mine - Mine coins (secret)\n"
        "/farm - Farm coins (secret)\n"
        "/crime - Commit a crime to earn coins (secret)\n"
        "/heal - Heal yourself (secret)\n"
        "/shop - Access the secret shop (secret)\n"
        "/buy - Buy items from secret shop (secret)\n"
        "/sell - Sell items to secret shop (secret)\n"
        "/profile - See hidden profile stats (secret)\n"
        "/bank - Check hidden bank balance (secret)\n"
        "/deposit - Deposit coins in secret bank (secret)\n"
        "/withdraw - Withdraw coins from secret bank (secret)\n"
    )

    await update.message.reply_text(help_text, parse_mode="Markdown")
