import os
from telegram import Update
from telegram.ext import CallbackContext
from database.users import get_user, users  # database folder se import

# Load the owner ID from environment variables
try:
    OWNER_ID = int(os.getenv("OWNER_ID"))
except (TypeError, ValueError):
    OWNER_ID = 8379938997  # fallback owner ID

async def transfer_balance(update: Update, context: CallbackContext):
    """
    Allows the bot owner to manually add or remove coins from a user's balance.
    Command format: /transfer <amount> (in reply) or /transfer <user_id> <amount>
    Use negative amount to remove coins (e.g., -500).
    """
    
    # 1️⃣ Owner Check
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("🚫 This command is reserved for the bot owner only.")
        return

    args = context.args
    target_user_id = None
    amount = None

    # 2️⃣ Parse Target & Amount
    if update.message.reply_to_message:
        if len(args) == 1:
            try:
                amount = int(args[0])
                target_user_id = update.message.reply_to_message.from_user.id
            except ValueError:
                await update.message.reply_text("❌ Invalid amount. Usage: `/transfer <amount>` (reply).")
                return
        else:
            await update.message.reply_text("❌ Missing amount. Usage: `/transfer <amount>` (reply).")
            return
    elif len(args) == 2:
        try:
            target_user_id = int(args[0])
            amount = int(args[1])
        except ValueError:
            await update.message.reply_text("❌ Invalid user ID or amount. Usage: `/transfer <user_id> <amount>`.")
            return
    else:
        await update.message.reply_text("❌ Invalid usage. Use: `/transfer <amount>` (reply) or `/transfer <user_id> <amount>`.")
        return

    # 3️⃣ Execute Transfer
    try:
        target_user = get_user(target_user_id)
        users.update_one({"user_id": target_user_id}, {"$inc": {"balance": amount}})
        updated_user = get_user(target_user_id)
        new_balance = updated_user['balance']

        action = "added to" if amount >= 0 else "removed from"

        await update.message.reply_text(
            f"✅ *Success!* \n"
            f"${abs(amount)} has been *{action}* user `{target_user_id}`'s balance "
            f"(Name: {target_user.get('username', 'N/A')}).\n"
            f"New Balance: ${new_balance}",
            parse_mode="Markdown"
        )

    except Exception as e:
        print(f"Transfer error for user {target_user_id}: {e}")
        await update.message.reply_text(
            "❌ An error occurred during the transfer. "
            "The target user might not be registered in the economy yet."
        )
