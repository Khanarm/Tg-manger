from telethon import events, Button

from config import OWNER_ID
from userbot.channel import get_all_channels


COMMANDS = {
    "/setname": "setname",
    "/setbio": "setbio",
    "/setusername": "setusername",
    "/setphoto": "setphoto",
}


def register(bot):

    @bot.on(events.NewMessage(pattern=r"^/(setname|setbio|setusername|setphoto)$"))
    async def channel_menu(event):

        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized.")
            return

        action = COMMANDS[event.raw_text]

        channels = await get_all_channels()

        if not channels:
            await event.reply("❌ No channels found.")
            return

        buttons = []

        for channel in channels:
            buttons.append([
                Button.inline(
                    channel["title"],
                    data=f"{action}:{channel['channel_id']}".encode()
                )
            ])

        await event.reply(
            "📢 Select a Channel",
            buttons=buttons
        )
