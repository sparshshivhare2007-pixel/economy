# =====================================================
#                BROADCAST WITH FORWARD + TEXT
# =====================================================
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("⛔ You are not authorized.")

    msg = update.message
    sent = 0
    failed = 0

    # ------------------------------------------------
    # MODE 1: REPLY → FORWARD BROADCAST
    # ------------------------------------------------
    if msg.reply_to_message:
        original = msg.reply_to_message

        await msg.reply_text("📣 Forward broadcast started...")

        # ---------- USERS ----------
        for u in users.find():
            try:
                await original.forward(chat_id=u["user_id"])
                sent += 1
                await asyncio.sleep(0.03)
            except:
                failed += 1

        # ---------- GROUPS ----------
        for g in groups_db.find():
            try:
                await original.forward(chat_id=g["group_id"])
                sent += 1
                await asyncio.sleep(0.03)
            except:
                failed += 1

        return await msg.reply_text(
            f"📢 <b>Forward Broadcast Completed</b>\n\n"
            f"✅ Sent: {sent}\n"
            f"❌ Failed: {failed}",
            parse_mode="HTML"
        )

    # ------------------------------------------------
    # MODE 2: NORMAL TEXT BROADCAST
    # ------------------------------------------------
    if not context.args:
        return await msg.reply_text(
            "⚠️ Usage:\n"
            "/broadcast <text>\n"
            "OR reply to any message and send /broadcast"
        )

    text = " ".join(context.args)

    await msg.reply_text("📣 Text broadcast started...")

    # ---------- USERS ----------
    for u in users.find():
        try:
            await context.bot.send_message(u["user_id"], text, parse_mode="HTML")
            sent += 1
            await asyncio.sleep(0.03)
        except:
            failed += 1

    # ---------- GROUPS ----------
    for g in groups_db.find():
        try:
            await context.bot.send_message(g["group_id"], text, parse_mode="HTML")
            sent += 1
            await asyncio.sleep(0.03)
        except:
            failed += 1

    return await msg.reply_text(
        f"📢 <b>Broadcast Completed</b>\n\n"
        f"✅ Sent: {sent}\n"
        f"❌ Failed: {failed}",
        parse_mode="HTML"
    )
