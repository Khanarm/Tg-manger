from telethon import TelegramClient
from telethon.sessions import StringSession

from config import API_ID, API_HASH
from database.mongo import get_all_userbots

# Store all running clients
clients = {}


async def start_userbots():
    """
    Start all saved userbots from MongoDB.
    """
    bots = await get_all_userbots()

    for bot in bots:
        try:
            session = bot["session"]
            user_id = bot["user_id"]

            client = TelegramClient(
                StringSession(session),
                API_ID,
                API_HASH
            )

            await client.start()

            me = await client.get_me()

            clients[user_id] = client

            print(f"✅ UserBot Started : {me.first_name} ({user_id})")

        except Exception as e:
            print(f"❌ Failed to start UserBot {bot.get('user_id')}")
            print(e)


def get_client(user_id: int):
    """
    Return running client by userbot id.
    """
    return clients.get(user_id)


def get_all_clients():
    """
    Return all running clients.
    """
    return clients
