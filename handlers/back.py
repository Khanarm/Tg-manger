from telethon import events, Button

from config import OWNER_ID
from userbot.channel import get_all_channels

COMMANDS = {
    "setname": "setname",
    "setbio": "setbio",
    "setusername": "setusername",
    "setphoto": "setphoto",
}


def register(bot):

    @bot.on(events.CallbackQuery(pattern=b"back:"))
    async def back_handler(event):

        if event.sender_id != OWNER_ID:
            return

        data = event.data.decode()

        _, action = data.split(":")

        channels = await get_all_channels()

        if not channels:
            await event.edit("❌ No channels found.")
            return

        buttons = []

        for channel in channels:
            buttons.append([
                Button.inline(
                    channel["title"],
                    data=f"{action}:{channel['channel_id']}".encode()
                )
            ])

        await event.edit(
            "📢 Select a Channel",
            buttons=buttons
      )
