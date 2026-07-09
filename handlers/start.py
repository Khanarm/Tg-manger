from telethon import events, Button
from config import OWNER_ID


def register(bot):

    @bot.on(events.NewMessage(pattern="/start"))
    async def start(event):

        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized.")
            return

        buttons = [
            [Button.text("/setname", resize=True)],
            [Button.text("/setbio", resize=True)],
            [Button.text("/setusername", resize=True)],
            [Button.text("/setphoto", resize=True)],
            [Button.text("/broadcast", resize=True)],
        ]

        await event.reply(
            "🤖 **Telegram Channel Manager**\n\n"
            "Welcome!\n\n"
            "Choose a command below.",
            buttons=buttons
        )
