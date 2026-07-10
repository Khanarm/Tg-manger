from telethon import events

from config import OWNER_ID
from state import pending_actions

from userbot.channel import (
    set_channel_name,
    set_channel_bio,
    set_channel_username,
)


def register(bot):

    @bot.on(events.NewMessage)
    async def message_handler(event):

        if event.sender_id != OWNER_ID:
            return

        if event.sender_id not in pending_actions:
            return

        data = pending_actions[event.sender_id]

        action = data["action"]
        channel_id = data["channel_id"]

        text = event.raw_text.strip()

        success = False

        if action == "setname":
            success = await set_channel_name(channel_id, text)

        elif action == "setbio":
            success = await set_channel_bio(channel_id, text)

        elif action == "setusername":
            success = await set_channel_username(channel_id, text)

        if success:
            await event.reply("✅ Updated Successfully.")
        else:
            await event.reply("❌ Update Failed.")

        pending_actions.pop(event.sender_id, None)
