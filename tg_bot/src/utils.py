from aiogram.exceptions import TelegramBadRequest
from app import bot


async def renew_message(chat_id, message_id, text, reply_markup=None) -> None:
    try:
        await bot.delete_message(chat_id, message_id)
    except TelegramBadRequest:
        pass
    await bot.send_message(chat_id, text, reply_markup=reply_markup)


async def renew_photo_message(chat_id, message_id, text, photo, reply_markup=None) -> None:
    try:
        await bot.delete_message(chat_id, message_id)
    except TelegramBadRequest:
        pass
    await bot.send_photo(chat_id, photo=photo, caption=text, reply_markup=reply_markup)
