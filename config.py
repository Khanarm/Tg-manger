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

MONGO_URI = "mongodb+srv://ansaritohib562_db_user:QAG8UQswaXgqu8hN@cluster0.kr0ng3d.mongodb.net/?appName=Cluster0"

DATABASE_NAME = "channel_manager"
