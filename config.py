import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

OWNER_ID = int(os.getenv("OWNER_ID"))

STRING_SESSIONS = []

for key, value in os.environ.items():
    if key.startswith("STRING_SESSION_") and value:
        STRING_SESSIONS.append(value)

MONGO_URL = ""

DATABASE_NAME = "channel_manager"
