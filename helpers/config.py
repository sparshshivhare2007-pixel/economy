# helpers/config.py
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID", "0"))
MONGO_URI = os.getenv("MONGO_URI")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "")
GIT_TOKEN = os.getenv("GIT_TOKEN", "")
