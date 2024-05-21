from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import BufferedInputFile

import asyncio

from app import bot
from config import settings
from utils import renew_message, renew_photo_message
from services.photo.get_photo_from_static import get_photo_info
from services.db.repository import repository
from services.menu.main_menu import main_menu
from services.menu.catalog import form_catalog_menu, form_category_menu, form_subcategory_menu, form_basket_menu, form_product_markup

router = Router()

@router.message(Command("menu"))
@router.message(Command("start"))
async def get_start(message: Message):
    user_channel_status = await bot.get_chat_member(chat_id=settings.CHANNEL_ID, user_id=message.from_user.id)
    user_group_status = await bot.get_chat_member(chat_id=settings.GROUP_ID, user_id=message.from_user.id)
    if user_channel_status.status == 'left' or user_group_status.status == 'left':
        return await message.answer(f'Необходимо присутствовать в канале {settings.CHANNEL_ID} и группе {settings.GROUP_ID}')
    
    await message.answer('Доступные команды:', reply_markup=main_menu)


@router.callback_query(F.data.startswith('m'))
async def get_categories(call: CallbackQuery):
    await renew_message(call.from_user.id, call.message.message_id, 'Доступные команды:', reply_markup=main_menu)

@router.callback_query(F.data.startswith('k'))
async def get_categories(call: CallbackQuery):
    offset, limit, prev = call.data.split(':')[1:]
    await renew_message(call.from_user.id, call.message.message_id, 'Каталог:', (await form_catalog_menu(int(offset), int(limit), call.data)))


@router.callback_query(F.data.startswith('c'))
async def get_subcategories(call: CallbackQuery):
    id, offset, limit, prev = call.data.split(':')[1:]
    await renew_message(call.from_user.id, call.message.message_id, 'Каталог:', (await form_category_menu(int(id), int(offset), int(limit), call.data)))


@router.callback_query(F.data.startswith('s'))
async def get_products(call: CallbackQuery):
    id, offset, limit, prev = call.data.split(':')[1:]
    await renew_message(call.from_user.id, call.message.message_id, 'Каталог:', (await form_subcategory_menu(int(id), int(offset), int(limit), call.data)))


@router.callback_query(F.data.startswith('b'))
async def get_basket(call: CallbackQuery):
    offset, limit, prev = call.data.split(':')[1:]
    await renew_message(call.from_user.id, call.message.message_id, 'Каталог:', (await form_basket_menu(int(call.from_user.id), int(offset), int(limit), call.data)))


@router.callback_query(F.data.startswith('p'))
async def get_product(call: CallbackQuery):
    id = call.data.split(':')[1]
    text, photo, markup = await get_photo_info(call.from_user.id, int(id), call.data)
    await renew_photo_message(call.from_user.id, call.message.message_id, text=text, photo=photo, reply_markup=markup)


@router.callback_query(F.data.startswith('quantity'))
async def change_quantity(call: CallbackQuery):
    product_id, q, prev = call.data.split(':')[1:]
    await repository.create_basket_if_not_exist(call.from_user.id)

    await repository.update_quantity(call.from_user.id, product_id, q)

    text, photo, markup = await get_photo_info(call.from_user.id, int(product_id), prev)
    await renew_photo_message(call.from_user.id, call.message.message_id, text=text, photo=photo, reply_markup=markup)


@router.callback_query(F.data.startswith('add'))
async def change_quantity(call: CallbackQuery):
    product_id, prev = call.data.split(':')[1:]
    await repository.create_basket_if_not_exist(call.from_user.id)

    await repository.add_product_in_backet(call.from_user.id, int(product_id))

    text, photo, markup = await get_photo_info(call.from_user.id, int(product_id), prev)
    await renew_photo_message(call.from_user.id, call.message.message_id, text=text, photo=photo, reply_markup=markup)


@router.message()
async def echo(message: Message):
    await message.answer(message.text)


