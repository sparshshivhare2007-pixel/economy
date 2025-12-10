# helpers/utils.py
import html
import random
from typing import Tuple, Optional, Dict, Any
from telegram import Update
from telegram.ext import ContextTypes

# GLOBAL SUDO LIST (loaded from DB)
SUDO_USERS = []


# -------------------------------------------------
# 1) RANDOM PERCENTAGE (Love, Crush, etc.)
# -------------------------------------------------
def random_percentage() -> int:
    return random.randint(1, 100)


# -------------------------------------------------
# 2) MONEY FORMATTER
# -------------------------------------------------
def format_money(amount: int) -> str:
    try:
        return f"${int(amount):,}"
    except:
        return str(amount)


# -------------------------------------------------
# 3) FANCY FONT (RyanBaka style aesthetic)
# -------------------------------------------------
def stylize_text(text: str) -> str:
    font_map = {
        'A':'ᴧ','B':'ʙ','C':'ᴄ','D':'ᴅ','E':'Є','F':'Ғ','G':'ɢ',
        'H':'ʜ','I':'ɪ','J':'ᴊ','K':'ᴋ','L':'ʟ','M':'ϻ','N':'η',
        'O':'σ','P':'ᴘ','Q':'ǫ','R':'ᴚ','S':'s','T':'ᴛ','U':'υ',
        'V':'ᴠ','W':'ᴡ','X':'x','Y':'ʏ','Z':'ᴢ',
        'a':'ᴧ','b':'ʙ','c':'ᴄ','d':'ᴅ','e':'є','f':'ғ','g':'ɢ',
        'h':'ʜ','i':'ɪ','j':'ᴊ','k':'ᴋ','l':'ʟ','m':'ϻ','n':'η',
        'o':'σ','p':'ᴘ','q':'ǫ','r':'ʀ','s':'s','t':'ᴛ','u':'υ',
        'v':'ᴠ','w':'ᴡ','x':'x','y':'ʏ','z':'ᴢ',
        '0':'𝟎','1':'𝟏','2':'𝟐','3':'𝟑','4':'𝟒','5':'𝟓',
        '6':'𝟔','7':'𝟕','8':'𝟖','9':'𝟗'
    }
    return "".join(font_map.get(c, c) for c in str(text))


# -------------------------------------------------
# 4) GET MENTION (HTML Safe)
# -------------------------------------------------
def get_mention(user: Dict[str, Any]) -> str:
    try:
        uid = user.get("user_id")
        name = user.get("first_name") or user.get("name") or "User"
        return f"<a href='tg://user?id={uid}'><b>{html.escape(str(name))}</b></a>"
    except:
        return "<b>User</b>"


# -------------------------------------------------
# 5) TARGET RESOLVER (Reply / ID / @username)
# -------------------------------------------------
async def resolve_target(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    specific_arg: Optional[str] = None
) -> Tuple[Optional[Dict], Optional[str]]:

    # A) REPLY TARGET
    if update.message and update.message.reply_to_message:
        u = update.message.reply_to_message.from_user
        return ({"user_id": u.id, "first_name": u.first_name}, None)

    # B) SPECIFIC ARGUMENT (ID / USERNAME)
    if specific_arg:

        # numeric ID
        if specific_arg.isdigit():
            return ({"user_id": int(specific_arg), "first_name": specific_arg}, None)

        # @username
        if specific_arg.startswith("@"):
            try:
                chat = await context.bot.get_chat(specific_arg)
                return (
                    {"user_id": chat.id, "first_name": getattr(chat, "first_name", specific_arg)},
                    None
                )
            except:
                return (None, "User not found by username.")

    # nothing found
    return (None, "No target found. Reply to a user or pass id/username.")


# -------------------------------------------------
# 6) SUDO RELOADER (RyanBaka Compatible)
# -------------------------------------------------
def reload_sudoers(mongo_db):
    """
    Load sudoers from MongoDB -> updates global SUDO_USERS list.
    """
    global SUDO_USERS
    SUDO_USERS = []

    try:
        # get collection
        sudo_col = (
            mongo_db.sudoers
            if hasattr(mongo_db, "sudoers")
            else mongo_db.get_collection("sudoers")
        )

        for d in sudo_col.find():
            uid = d.get("user_id")
            if uid:
                SUDO_USERS.append(int(uid))

    except Exception:
        pass
