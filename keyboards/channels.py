from aiogram.utils.keyboard import InlineKeyboardBuilder


def channels_keyboard(channels):

    builder = InlineKeyboardBuilder()

    for channel in channels:
        builder.button(
            text=channel.title,
            callback_data=f"channel_{channel.id}"
        )

    builder.adjust(1)

    return builder.as_markup()
