from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


start_buttons = [
    [InlineKeyboardButton(text='Каталог', callback_data='k:0:10:m')],
    [InlineKeyboardButton(text='Корзина', callback_data='b:0:10:m')],
]

main_menu = InlineKeyboardMarkup(inline_keyboard=start_buttons)