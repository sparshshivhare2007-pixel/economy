# database/chatbot.py
from . import db

chatai = db["chatai"]  # AI chat replies
lang_db = db["ChatLangDb"]  # chat languages
status_db = db["chatbot_status_db"]  # bot status per chat
