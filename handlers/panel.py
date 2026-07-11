from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import OWNER_ID
from userbot.client import get_all_channels, get_channel_info
from keyboards.panel import (
    panel_channels_keyboard,
    channel_info_keyboard,
)

router = Router()
