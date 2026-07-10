from telethon import events

from config import OWNER_ID
from state import pending_actions


MESSAGES = {
    "setname": "✏️ Send the new channel name.",
    "setbio": "📝 Send the new channel bio.",
    "setusername": "🌐 Send the new username.\n\nExample: mychannel",
    "setphoto": "🖼 Send the new channel photo.",
}


def register(bot):

    @bot.on(events.CallbackQuery(pattern=b"confirm:"))
    async def confirm_handler(event):

        if event.sender_id != OWNER_ID:
            return

        data = event.data.decode()

        _, action, channel_id = data.split(":")

        pending_actions[event.sender_id] = {
            "action": action,
            "channel_id": int(channel_id)
        }

        await event.edit(
            MESSAGES.get(action, "Send value.")
        )
