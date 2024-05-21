from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from services.db.repository import repository



def constuct_back_button_and_prev(prev: str) -> tuple[str]:
    track = prev.split(':')[-1]
    back = ''
    is_first_alpha = True
    for n, c in enumerate(track):
        if c.isalpha():
            if is_first_alpha:
                is_first_alpha = False
                back += c
            else:
                back += track[n:]
                break
        elif c == '.':
            back += ':'
        else:
            back += c

    prev = prev.replace(':', '.')
    return back, prev


def form_menu(current_prefix, next_prefix, instance_list, offset, limit, prev: str, id = None) -> InlineKeyboardMarkup:
    back, prev = constuct_back_button_and_prev(prev)
    buttons = []
    buttons.extend([[InlineKeyboardButton(text=title, callback_data=f'{next_prefix}:{id}:0:10:{prev}')] for id, title in instance_list])
    if offset and len(instance_list) == limit:
        buttons.extend([
            [
            InlineKeyboardButton(text='<', callback_data=f'{current_prefix}{f":{id}" if id else ""}:{max(0, offset - limit)}:10:{prev}'),
            InlineKeyboardButton(text='>', callback_data=f'{current_prefix}{f":{id}" if id else ""}:{offset + limit}:10:{prev}'),
            ],
            [InlineKeyboardButton(text='Назад', callback_data=back)]
        ])
    elif offset:
        buttons.extend([
            [
            InlineKeyboardButton(text='<', callback_data=f'{current_prefix}{f":{id}" if id else ""}:{max(0, offset - limit)}:10:{prev}'),
            ],
            [InlineKeyboardButton(text='Назад', callback_data=back)]
        ])
    elif len(instance_list) == limit:
        buttons.extend([
            [
            InlineKeyboardButton(text='>', callback_data=f'{current_prefix}{f":{id}" if id else ""}:{offset + limit}:10:{prev}')
            ],
            [InlineKeyboardButton(text='Назад', callback_data=back)]
        ])
    else:
        buttons.append([InlineKeyboardButton(text='Назад', callback_data=back)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def form_catalog_menu(offset, limit, prev):
    instance_list = await repository.get_categories(offset, limit)
    return form_menu('k', 'c', instance_list, offset, limit, prev)

async def form_category_menu(id, offset, limit, prev):
    instance_list = await repository.get_subcategories_from_categories(id, offset, limit)
    return form_menu('c', 's', instance_list, offset, limit, prev, id)

async def form_subcategory_menu(id, offset, limit, prev):
    instance_list = await repository.get_products_in_subcategories(id, offset, limit)
    return form_menu('s', 'p', instance_list, offset, limit, prev, id)

async def form_basket_menu(user_id, offset, limit, prev):
    back, prev = constuct_back_button_and_prev(prev)
    product_list = await repository.get_products_from_basket(user_id, offset, limit)
    buttons = []

    [
        [
            buttons.append([InlineKeyboardButton(text=title, callback_data=f'p:{id}:{prev}')]),
            buttons.append([
                InlineKeyboardButton(text='-', callback_data=f'quantity:{id}:{quantity-1}'), 
                InlineKeyboardButton(text='-5', callback_data=f'quantity:{id}:{quantity-5}'), 
                InlineKeyboardButton(text=str(quantity), callback_data='null'), 
                InlineKeyboardButton(text='+5', callback_data=f'quantity:{id}:{quantity+5}'),
                InlineKeyboardButton(text='+', callback_data=f'quantity:{id}:{quantity+1}'),
            ])
        ] for id, title, quantity in product_list
    ]
    if offset and len(product_list) == limit:
        buttons.extend([
            [
            InlineKeyboardButton(text='<', callback_data=f'b:{max(0, offset - limit)}:10:{prev}'),
            InlineKeyboardButton(text='>', callback_data=f'b:{offset + limit}:10:{prev}'),
            ],
        ])
    elif offset:
        buttons.extend([
            [
            InlineKeyboardButton(text='<', callback_data=f'b:{max(0, offset - limit)}:10:{prev}'),
            ],
        ])
    elif len(product_list) == limit:
        buttons.extend([
            [
            InlineKeyboardButton(text='>', callback_data=f'b:{offset + limit}:10:{prev}'),
            ],
        ])
    
    buttons.append([InlineKeyboardButton(text='Назад', callback_data=back)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def form_product_markup(user_id: int, product_id: int, prev) -> InlineKeyboardMarkup:
    #prev = prev.split(':')[-1]
    back, prev = constuct_back_button_and_prev(prev)
    buttons = []
    quantity = await repository.get_product_from_basket(user_id, product_id)
    if not quantity:
        buttons.append(
            [InlineKeyboardButton(text='Добавить продукт', callback_data=f'add:{product_id}:{prev}')]
        )
    else:
        buttons.append(
                [
                InlineKeyboardButton(text='-', callback_data=f'quantity:{product_id}:{quantity-1}:{prev}'), 
                InlineKeyboardButton(text='-5', callback_data=f'quantity:{product_id}:{quantity-5}:{prev}'), 
                InlineKeyboardButton(text=str(quantity), callback_data='null'), 
                InlineKeyboardButton(text='+5', callback_data=f'quantity:{product_id}:{quantity+5}:{prev}'),
                InlineKeyboardButton(text='+', callback_data=f'quantity:{product_id}:{quantity+1}:{prev}')
                ]
            )
        
    buttons.append([InlineKeyboardButton(text='Назад', callback_data=back)])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)