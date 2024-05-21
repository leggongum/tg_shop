import aiohttp

from aiogram.types.input_file import BufferedInputFile
from services.db.repository import repository
from services.menu.catalog import form_product_markup

async def get_photo(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://nginx:8000/{url}') as resp:
            if resp.status == 200:
                return await resp.read()


async def get_photo_info(user_id, id, call_data):
    title, description, price, image, amount = await repository.get_product(int(id))
    text = f'<b>{title}</b>\n{description}\n\n{price}₽'
    photo = BufferedInputFile(file=await get_photo(image), filename=image.split('/')[-1])
    markup = await form_product_markup(user_id, int(id), call_data)

    return text, photo, markup