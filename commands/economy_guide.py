# commands/economy_guide.py

from telegram import Update
from telegram.ext import ContextTypes

async def economy_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Full Akeno Economy + Secret + Elite Command Guide."""

    text = (
        "✨ 👀myra Universal Economy Guide👀 ✨\n"
        "=========================================\n\n"

        "👋 *Welcome to myra Economy System!*\n"
        "यह guide आपके bot की सारी Public + Secret + Elite economy commands को एक जगह detail में बताती है।\n\n"

        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "💰 *Public Economy Commands*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔹 `/bal` — अपनी/दोस्त की balance देखो\n"
        "🔹 `/toprich` — सबसे अमीर top 10 users\n"
        "🔹 `/topkill` — Top 10 killers\n"
        "🔹 `/give amount` (reply) — पैसे gift करो\n"
        "🔹 `/rob amount` (reply) — Lootne की कोशिश\n"
        "🔹 `/kill` (reply) — User को kill करके पैसा पाओ\n"
        "🔹 `/revive` — खुद को/दोस्त को revive करो\n"
        "🔹 `/protect 1d|2d` — सुरक्षा खरीदो (anti-rob)\n"
        "🔹 `/daily` — Daily reward claim करो\n"
        "🔹 `/work` — काम करके पैसे कमाओ\n"
        "🔹 `/items` — सभी items की list\n"
        "🔹 `/item itemname` — Item details\n"
        "🔹 `/give` — Item gift करो\n"
        "🔹 `/slap` `/punch` `/hug` `/couple` — Fun commands\n\n"

        "📛 *Admin Economy Control*\n"
        "🔹 `/open` — Economy चालू करो\n"
        "🔹 `/close` — Economy बंद करो\n"
        "🔹 `/transfer amount` — Owner: Money add/remove\n\n"

        "=========================================\n"
        "🕵️ *SECRET ELITE COMMANDS (Hidden)*\n"
        "=========================================\n"
        "यह commands आम users नहीं जानते। सिर्फ pro/dark economy users।\n\n"

        "🌑 *Dark Economy System*\n"
        "🔹 `/hack` — Random user से चोरी की कोशिश (chance-based)\n"
        "🔹 `/blackmail` (reply) — डराकर पैसे निकलवाना\n"
        "🔹 `/smuggle` — Illegal पैसे कमाओ (high risk)\n"
        "🔹 `/bribe` — Fine हटवाने के लिए police को bribe\n"
        "🔹 `/spy` (reply) — Secret stats निकालने की कोशिश\n\n"

        "🎲 *Risk | Gamble | High Stakes*\n"
        "🔹 `/double amount` — पैसा double करने का risky तरीका\n"
        "🔹 `/risk amount` — Jackpot gamble\n"
        "🔹 `/dicefight amount` (reply) — Dice war (winner gets all)\n"
        "🔹 `/duel amount` (reply) — 1v1 battle for money\n\n"

        "👁‍🗨️ *Secret Utility Commands*\n"
        "🔹 `/profile` — Hidden profile देखें\n"
        "🔹 `/inventory` — अपनी items list\n"
        "🔹 `/steal` (reply) — Item चोरी करने की कोशिश\n"
        "🔹 `/bank` — Bank balance देखें\n"
        "🔹 `/deposit amount` — पैसे bank में जमा\n"
        "🔹 `/withdraw amount` — पैसे bank से निकालो\n\n"

        "=========================================\n"
        "⚠️ *OWNER ONLY SECRET COMMANDS*\n"
        "=========================================\n"
        "🔹 `/resetbal` (reply) — User का balance zero\n"
        "🔹 `/setbal amount` (reply) — Direct balance set\n"
        "🔹 `/resetkills` — Kill count reset\n"
        "🔹 `/wipeecon` — FULL economy wipe (Dangerous)\n\n"

        "=========================================\n"
        "🔥 *PRO TIPS*\n"
        "=========================================\n"
        "• Smuggle/Hack risky है— पकड़े गए तो बड़ा नुकसान\n"
        "• Bank में पैसा सबसे safe — robbery नहीं होती\n"
        "• Spy command सिर्फ *40% chance* पर successful होती है\n"
        "• Dicefight और Duel fastest earning method हैं\n"
        "• Protection खरीदे बिना robbery से बच नहीं सकते\n\n"

        "✨ *Welcome to myra Elite Economy.* ✨"
    )

    await update.message.reply_text(text, parse_mode="Markdown")
