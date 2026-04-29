import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "your_username")

if not TOKEN:
    raise SystemExit("Set TELEGRAM_BOT_TOKEN in .env")
if not ADMIN_CHAT_ID:
    raise SystemExit("Set ADMIN_CHAT_ID in .env")

DB_PATH = os.getenv("DB_PATH", "bot_requests.db")