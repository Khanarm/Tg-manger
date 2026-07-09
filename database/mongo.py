from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DATABASE_NAME

client = AsyncIOMotorClient(MONGO_URI)

db = client[DATABASE_NAME]

users = db.users
channels = db.channels
settings = db.settings
userbots = db.userbots
broadcasts = db.broadcasts
