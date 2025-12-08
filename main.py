# main.py
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# -------------------- DATABASE --------------------
from database.users import (
    get_user,
    user_db,
    add_group_id,
    add_message_count,
    users,
    groups_db
)

# -------------------- LOAD ENV --------------------
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID", "0"))

# -------------------- IMPORT COMMANDS --------------------
from commands.start_command import start_command, button_handler
from commands.group_management import register_group_management  

from commands.economy_guide import economy_guide
from commands.help_command import help_command  
from commands.transfer_balance import transfer_balance
from commands.claim import claim
from commands.own import own
from commands.crush import crush
from commands.love import love
from commands.slap import slap
from commands.items import items
from commands.item import item
from commands.give import give
from commands.daily import daily
from commands.rob import rob
from commands.protect import protect
from commands.toprich import toprich
from commands.topkill import topkill
from commands.kill import kill
from commands.revive import revive
from commands.open_economy import open_economy
from commands.close_economy import close_economy
from commands.punch import punch
from commands.hug import hug
from commands.couple import couple
from commands.mine import mine
from commands.farm import farm
from commands.crime import crime
from commands.heal import heal
from commands.shop import shop
from commands.buy import buy
from commands.sell import sell
from commands.profile import profile
from commands.bank import bank
from commands.deposit import deposit
from commands.withdraw import withdraw

# AI Chat
from commands.chat import chat_handler


# =====================================================
#                   BROADCAST SYSTEM
# =====================================================
import asyncio

# -------- NORMAL BROADCAST ----------
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("⛔ You are not authorized.")

    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /broadcast <message>")

    text = " ".join(context.args)
    sent = 0
    failed = 0

    for u in users.find():
        try:
            await context.bot.send_message(u["user_id"], text)
            sent += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1

    for g in groups_db.find():
        try:
            await context.bot.send_message(g["group_id"], text)
            sent += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1

    await update.message.reply_text(
        f"📢 <b>Broadcast Completed</b>\n\n"
        f"✅ Sent: {sent}\n"
        f"❌ Failed: {failed}",
        parse_mode="HTML"
    )


# -------- REPLY-STYLE BROADCAST ----------
async def replycast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("⛔ You are not authorized.")

    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /replycast <message>")

    text = " ".join(context.args)

    reply_message = (
        f"💬 <b>Broadcast Reply</b>\n"
        f"<i>(Looks like a reply, not forwarded)</i>\n\n"
        f"{text}"
    )

    sent = 0
    failed = 0

    for u in users.find():
        try:
            await context.bot.send_message(u["user_id"], reply_message, parse_mode="HTML")
            sent += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1

    for g in groups_db.find():
        try:
            await context.bot.send_message(g["group_id"], reply_message, parse_mode="HTML")
            sent += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1

    await update.message.reply_text(
        f"📢 <b>Replycast Completed</b>\n\n"
        f"✅ Sent: {sent}\n"
        f"❌ Failed: {failed}",
        parse_mode="HTML"
    )


# =====================================================


# -------------------- AUTO RESTART --------------------
async def test_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("⛔ You are not authorized.")
    await update.message.reply_text("🔄 Restarting bot...")
    os._exit(1)


# -------------------- TRACK USERS --------------------
async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    add_group_id(chat.id)

    if chat.type == "private":
        try:
            await context.bot.send_message(
                ADMIN_GROUP_ID,
                f"👤 <a href='tg://user?id={user.id}'>{user.first_name}</a> started the bot.",
                parse_mode="HTML"
            )
        except:
            pass


# -------------------- BALANCE --------------------
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        user_id = target.id
        name = target.first_name
    else:
        user_id = update.effective_user.id
        name = update.effective_user.first_name

    user = get_user(user_id)
    rank_data = list(user_db.find().sort("balance", -1))
    ids = [u["user_id"] for u in rank_data]
    rank = ids.index(user_id) + 1 if user_id in ids else len(ids) + 1
    status = "☠️ Dead" if user.get("killed") else "Alive"

    await update.message.reply_text(
        f"👤 Name: {name}\n"
        f"💰 Balance: ${user['balance']}\n"
        f"🏆 Rank: #{rank}\n"
        f"❤️ Status: {status}\n"
        f"⚔️ Kills: {user['kills']}"
    )


# -------------------- WORK --------------------
async def work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    reward = 200
    user_db.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": reward}})
    await update.message.reply_text(f"💼 You worked and earned {reward} coins!")


# -------------------- ERROR HANDLER --------------------
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print("\n⚠️ ERROR OCCURRED ⚠️")
    print(context.error)
    print("------------------------------------\n")


# -------------------- AI + XP MESSAGE HANDLER --------------------
async def ai_group_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    text = msg.text.lower()

    add_message_count(msg.from_user.id)

    if msg.chat.type == "private":
        return await chat_handler(update, context)

    if context.bot.username.lower() in text:
        return await chat_handler(update, context)

    if msg.reply_to_message and msg.reply_to_message.from_user.id == context.bot.id:
        return await chat_handler(update, context)

    return


# -------------------- MAIN --------------------
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_error_handler(error_handler)

    # Track users
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, track_users))

    # /start
    app.add_handler(CommandHandler("start", start_command))

    # Buttons
    app.add_handler(CallbackQueryHandler(button_handler))

    # Restart
    app.add_handler(CommandHandler("test", test_restart))

    # Broadcast Commands
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("replycast", replycast))

    # Economy commands
    economy_commands = [
        ("balance", balance), ("work", work), ("economy", economy_guide),
        ("transfer", transfer_balance), ("claim", claim), ("own", own),
        ("crush", crush), ("love", love), ("slap", slap), ("items", items),
        ("item", item), ("give", give), ("daily", daily), ("rob", rob),
        ("protect", protect), ("toprich", toprich), ("topkill", topkill),
        ("kill", kill), ("revive", revive), ("open", open_economy),
        ("close", close_economy)
    ]
    for cmd, h in economy_commands:
        app.add_handler(CommandHandler(cmd, h))

    # Hidden commands
    hidden_cmds = [
        ("mine", mine), ("farm", farm), ("crime", crime), ("heal", heal),
        ("shop", shop), ("buy", buy), ("sell", sell),
        ("profile", profile), ("bank", bank),
        ("deposit", deposit), ("withdraw", withdraw)
    ]
    for cmd, h in hidden_cmds:
        app.add_handler(CommandHandler(cmd, h))

    # Fun commands
    fun_commands = [("punch", punch), ("hug", hug), ("couple", couple)]
    for cmd, h in fun_commands:
        app.add_handler(CommandHandler(cmd, h))

    # Group Management
    register_group_management(app)

    # AI + XP
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_group_filter))

    print("🚀 Bot Started Successfully!")
    app.run_polling()


if __name__ == "__main__":
    main()
