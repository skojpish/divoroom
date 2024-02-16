from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import FSInputFile, CallbackQuery, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.data_bases.psql_get import db_instock
from bot.keyboards.user_kbs import empty_inst_kb

router = Router()

# Get items in stock
class InStockCF(CallbackData, prefix="instock", sep="_"):
    item_id: int = 0

class NextTenCF(CallbackData, prefix="next", sep="_"):
    starting_point: int = 0
    next_ten: bool = False

class BuyInstCF(CallbackData, prefix="binst", sep="_"):
    name: str
    price: int

@router.callback_query(F.data == "instock")
async def in_stock10(callback: CallbackQuery) -> None:
    items10 = []
    items_id = []
    items_name = []
    items_next = False

    data = await db_instock.get_data10()

    if not data:
        await callback.message.answer("Работ в наличии нет, но вы можете заказать свой дизайн ниже", reply_markup=empty_inst_kb())
    else:
        for row in data:
            item_id = row[0]
            name = row[3]
            photo = row[4]
            image_id = row[7]
            name_image_id = row[10]

            if image_id is None or name_image_id != photo:
                items10.append(InputMediaPhoto(type='photo', media=FSInputFile(f"django_admin/proj/media/{photo}")))
            else:
                items10.append(InputMediaPhoto(type='photo', media=f'{image_id}'))

            items_id.append(item_id)
            items_name.append(name)

        if len(items10) > 9:
            items_next = True

        def kb_build10() -> InlineKeyboardMarkup:
            kb10 = InlineKeyboardBuilder()
            for i in range(len(items10)):
                kb10.button(
                    text=f"{i+1}", callback_data=InStockCF(item_id=items_id[i])
                )
            if items_next:
                kb10.button(
                    text=f"Посмотреть еще", callback_data=NextTenCF(next_ten=True, starting_point=10)
                )
            kb10.add(InlineKeyboardButton(
                text="Вернуться в главное меню", callback_data="back_to_menu"
            ))
            if len(items10) > 5:
                kb10.adjust(5, len(items10)-5, 1, 1)
            else:
                kb10.adjust(len(items10), 1)
            return kb10.as_markup()

        media_gr = await callback.message.answer_media_group(items10)

        for row in data:
            item_id = row[0]
            photo = row[4]
            image_id = row[7]
            name_image_id = row[10]

            if image_id is None or photo != name_image_id:
                image_id_cur = media_gr[data.index(row)].photo[-1].file_id
                await db_instock.add_image_id(item_id, image_id_cur, photo, 1)

        new_line = '\n'

        await callback.message.answer(f"<b>Работы в наличии</b>\n\n"
                                    f"{new_line.join([f'{items_name.index(name)+1}. '+str(name) for name in items_name])}\n\n"
                                      "Выберите номер понравившейся работы, чтобы узнать ее цену",
                                      reply_markup=kb_build10())
    await callback.answer()

@router.callback_query(NextTenCF.filter(F.next_ten==True))
async def in_stock20(callback: CallbackQuery, callback_data: NextTenCF) -> None:
    items20 = []
    items_id = []
    items_name = []
    items_next = False

    data = await db_instock.get_data_more(callback_data.starting_point)

    for row in data:
        item_id = row[0]
        name = row[3]
        photo = row[4]
        image_id = row[7]
        name_image_id = row[10]

        if image_id is None or name_image_id != photo:
            items20.append(InputMediaPhoto(type='photo', media=FSInputFile(f"django_admin/proj/media/{photo}")))
        else:
            items20.append(InputMediaPhoto(type='photo', media=f'{image_id}'))

        items_id.append(item_id)
        items_name.append(name)

    if len(items20) > 9:
        items_next = True

    def kb_build20() -> InlineKeyboardMarkup:
        kb20 = InlineKeyboardBuilder()
        for i in range(len(items20)):
            kb20.button(
                text=f"{i+1+callback_data.starting_point}", callback_data=InStockCF(item_id=items_id[i])
            )
        if items_next:
            kb20.button(
                text=f"Посмотреть еще", callback_data=NextTenCF(next_ten=True,
                                                                starting_point=callback_data.starting_point+10)
            )
        kb20.add(InlineKeyboardButton(
            text="Вернуться в главное меню", callback_data="back_to_menu"
        ))
        if len(items20) > 5:
            kb20.adjust(5, len(items20) - 5, 1, 1)
        else:
            kb20.adjust(len(items20), 1)
        return kb20.as_markup()

    media_gr = await callback.message.answer_media_group(items20)

    for row in data:
        item_id = row[0]
        photo = row[4]
        image_id = row[7]
        name_image_id = row[10]

        if image_id is None or name_image_id != photo:
            image_id_cur = media_gr[data.index(row)].photo[-1].file_id
            await db_instock.add_image_id(item_id, image_id_cur, photo, 1)

    new_line = '\n'

    await callback.message.answer(f"<b>Работы в наличии</b>\n\n"
        f"{new_line.join([f'{items_name.index(name)+1+callback_data.starting_point}. ' + str(name) for name in items_name])}\n\n"
        "Выберите номер понравившейся работы, чтобы узнать ее цену",
        reply_markup=kb_build20())
    await callback.answer()

# Callback handlers

@router.callback_query(InStockCF.filter())
async def in_stock_callbacks(callback: CallbackQuery, callback_data: InStockCF) -> None:
    row = await db_instock.get_specific_row(callback_data.item_id)
    data = {
        'name': row[3],
        'photo1': row[4],
        'photo2': row[5],
        'photo3': row[6],
        'price': row[1],
        'desc': row[2],
        'image_id1': row[7],
        'image_id2': row[8],
        'image_id3': row[9],
        'name_image_id1': row[10],
        'name_image_id2': row[11],
        'name_image_id3': row[12],
    }

    def buy_in_stock_kb() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.button(
            text=f"Купить", callback_data=BuyInstCF(name=data['name'], price=data['price'])
        )
        kb.add(InlineKeyboardButton(
            text="Заказать собственный дизайн", callback_data="order"
        ))
        kb.add(InlineKeyboardButton(
            text="Вернуться в главное меню", callback_data="back_to_menu"
        ))
        kb.adjust(1)
        return kb.as_markup()

    if data['photo2'] == '' and data['photo3'] == '':
        await callback.message.answer_photo(data['image_id1'], f"{data['name']}\n\n"
                                                            f"Цена: {data['price']} руб.\n\n"
                                                            f"{data['desc']}", reply_markup=buy_in_stock_kb())
        await callback.answer()
    else:
        media = []
        media.append(InputMediaPhoto(type='photo', media=data['image_id1']))

        if data['image_id2'] is None or data['name_image_id2'] != data['photo2']:
            media.append(InputMediaPhoto(type='photo', media=FSInputFile(f"django_admin/proj/media/{data['photo2']}")))
        else:
            media.append(InputMediaPhoto(type='photo', media=data['image_id2']))

        if data['image_id3'] is None or data['name_image_id3'] != data['photo3']:
            media.append(InputMediaPhoto(type='photo', media=FSInputFile(f"django_admin/proj/media/{data['photo3']}")))
        else:
            media.append(InputMediaPhoto(type='photo', media=data['image_id3']))

        media_gr = await callback.message.answer_media_group(media)

        if data['image_id2'] is None or data['name_image_id2'] != data['photo2']:
            image_id_cur = media_gr[1].photo[-1].file_id
            await db_instock.add_image_id(callback_data.item_id, image_id_cur, data['photo2'], 2)

        if data['image_id3'] is None or data['name_image_id3'] != data['photo3']:
            image_id_cur = media_gr[2].photo[-1].file_id
            await db_instock.add_image_id(callback_data.item_id, image_id_cur, data['photo3'], 3)

        await callback.message.answer(f"{data['name']}\n\n"
                                        f"Цена: {data['price']} руб.\n\n"
                                        f"{data['desc']}", reply_markup=buy_in_stock_kb())
        await callback.answer()

