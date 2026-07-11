from motor.motor_asyncio import AsyncIOMotorClient

from config import (
    MONGO_URI,
    DATABASE_NAME,
)

client = AsyncIOMotorClient(MONGO_URI)

db = client[DATABASE_NAME]

channels = db.channels
settings = db.settings
broadcast_logs = db.broadcast_logs
