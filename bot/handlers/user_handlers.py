from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.data_bases.fsm import IdeaState, DescripState, CityState, FullNameState, NumberState
from bot.data_bases.order import db_order
from bot.handlers.db_handlers import BuyInstCF

from bot.keyboards.edit_kbs import get_data_kb
from bot.keyboards.user_kbs import start_kb, back_to_menu_kb, budget_kb, choise_kb, material_kb, choise_country_kb, \
    confirm_order_kb, russia_delivery_kb, examples_kb, ex_kb, auto_delete_kb, about_kb

from bot.config import bot, master_id, master_username

router = Router()

async def auto_delete_user(user_id, username):
    try:
        row = await db_order.get_order_row(user_id)
        if row[1] is not None:
            await db_order.delete_user(user_id)
            await bot.send_message(user_id,
                               f"{username}, вы не отправили вашу заявку в течение суток, поэтому ваши данные были удалены. Если хотите отправить новую заявку, заполните данные заново🐥",
                               reply_markup=auto_delete_kb())
        else:
            pass
    except:
        pass

# Get start menu
@router.message(Command("start"))
async def cmd_start(msg: Message, state: FSMContext) -> None:
    await db_order.add_user_to_statistic(msg.from_user.id, msg.from_user.username, datetime.now())
    await state.clear()
    await msg.answer(f"Привет, {msg.from_user.full_name}!\n"
                                 f"Спасибо что заглянули в мой магазинчик🐣 В этом боте ты можешь сделать индивидуальный заказ или купить работы из наличия, посмотреть стоимость и отзывы🤍", reply_markup=start_kb())

# Start menu callbacks

@router.callback_query(F.data == "back_to_menu")
async def menu(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.delete_user(callback.from_user.id)
    await state.clear()
    await callback.message.answer(f"Привет, {callback.from_user.full_name}!\n"
                                    f"Спасибо что заглянули в мой магазинчик🐣 В этом боте ты можешь сделать индивидуальный заказ или купить работы из наличия, посмотреть стоимость и отзывы🤍", reply_markup=start_kb())
    await callback.answer()

@router.callback_query(F.data == "back")
async def menu(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await state.clear()
    await callback.answer()

@router.callback_query(F.data == "order")
async def choise_prices(callback: CallbackQuery) -> None:
    scheduler = AsyncIOScheduler()
    scheduler.configure({'apscheduler.daemon': False})
    scheduler.start()
    scheduler.add_job(auto_delete_user, 'date', run_date=datetime.now() + timedelta(hours=24),
                      kwargs={'user_id': callback.from_user.id, 'username': callback.from_user.full_name})

    await db_order.create_order_table()
    await db_order.add_user_to_db(callback.from_user.id)
    await callback.message.answer("Какой ваш примерный бюджет?", reply_markup=budget_kb())
    await callback.answer()

@router.callback_query(F.data == "examples")
async def examples(callback: CallbackQuery) -> None:
    await callback.message.answer("Примеры работ", reply_markup=examples_kb())
    await callback.answer()

@router.callback_query(F.data == "about")
async def about(callback: CallbackQuery) -> None:
    await callback.message.answer("Меня зовут Ада, мне 21 год, учусь на ✨реставрации живописи ✨ в Санкт-Петербурге\n\n"
                                  "Роспись вещей пришла в мою жизнь с лета 2022г. А вот рисую я сколько себя помню,"
                                  " и позиционирую себя  и как художник, и как кастомайзер🌛\n"
                                  "<i>Мне очень нравится воплощать ваши идеи, и дарить людям радость в обычных вещах</i> ☀\n\n"
                                  "Также я веду ТикТок (divoroom) на 175тыс.+ подписчиков, там много интересного!\n\n"
                                  "Если вы из Питера, то приехать забрать заказы можно лично🤲\n\n"
                                  "<i>Мне очень приятно, что вы заглянули в мой магазинчик, и надеюсь вернетесь еще и еще</i> 💓", reply_markup=about_kb())
    await callback.answer()

# Examples

@router.callback_query(F.data == "shoppers_ex")
async def shoppers_example(callback: CallbackQuery) -> None:
    await callback.message.answer("Примеры шопперов✨\n"
                                  "Цены на подобные работы от 3.5 тыс. руб.*\n\n"
                                  "* изделие входит в стоимость", reply_markup=ex_kb())
    await callback.answer()

@router.callback_query(F.data == "tshirts_ex")
async def tshirts_example(callback: CallbackQuery) -> None:
    await callback.message.answer("Примеры футболок✨\n"
                                  "Цены на подобные работы от 4 тыс. руб.*\n\n"
                                  "* изделие входит в стоимость", reply_markup=ex_kb())
    await callback.answer()

@router.callback_query(F.data == "hoodies_sweat_ex")
async def hoodies_example(callback: CallbackQuery) -> None:
    await callback.message.answer("Примеры худи и свитшотов✨\n"
                                  "Цены на подобные работы от 5 тыс. руб.*\n\n"
                                  "* изделие входит в стоимость", reply_markup=ex_kb())
    await callback.answer()

@router.callback_query(F.data == "pictures_ex")
async def pictures_example(callback: CallbackQuery) -> None:
    await callback.message.answer("Примеры картин✨\n"
                                  "Цены на подобные работы от 4 тыс. руб.*\n\n"
                                  "* изделие входит в стоимость", reply_markup=ex_kb())
    await callback.answer()

@router.callback_query(F.data == "badges_ex")
async def pictures_example(callback: CallbackQuery) -> None:
    await callback.message.answer("Примеры значков✨\n"
                                  "Цены на подобные работы 1.5 тыс. руб.*\n\n"
                                  "* изделие входит в стоимость", reply_markup=ex_kb())
    await callback.answer()
    
@router.callback_query(F.data == "other_cat")
async def other_cat(callback: CallbackQuery) -> None:
    await callback.message.edit_reply_markup(reply_markup=examples_kb())
    await callback.answer()

# Prices

@router.callback_query(F.data == "sum_13")
async def price_13(callback: CallbackQuery) -> None:
    await db_order.add_budget_db(callback.from_user.id, "1.5 - 3.5 тыс. руб.")
    await callback.message.answer("<b>1.5 - 3.5 тыс. руб.*</b>\n\n"
                                  "✨любые значки 1.5 тыс.\n"
                                  "✨шопперы с надписями/маленькими простыми иллюстрациями 2 - 3.5 тыс.\n\n"
                                  "* изделие входит в стоимость", reply_markup=choise_kb())
    await callback.answer()

@router.callback_query(F.data == "sum_35")
async def price_35(callback: CallbackQuery) -> None:
    await db_order.add_budget_db(callback.from_user.id, "3.5 - 5 тыс. руб.")
    await callback.message.answer("<b>3.5 - 5 тыс. руб.*</b>\n\n"
                                  "✨шопперы с иллюстрациями животных(одного), без фона, от 3.5 тыс\n"
                                  "✨шопперы с иллюстрациями животных(2 и больше), без фона, от 4 тыс \n"
                                  "✨шопперы с животными с фоном, от 4 тыс\n"
                                  "✨футболки с иллюстрациями 1-2 животных, ~5 тыс\n"
                                  "✨картины размером ~20х20 см, с однотонным фоном\n\n"
                                  "🐥все иллюстрации на другую тематику рассчитываются в "
                                  "зависимости от сложности, выбирайте просто по своему бюджету(также см. раздел «от 5тыс.»)\n\n"
                                  "* изделие входит в стоимость", reply_markup=choise_kb())
    await callback.answer()

@router.callback_query(F.data == "sum_5")
async def price_5(callback: CallbackQuery) -> None:
    await db_order.add_budget_db(callback.from_user.id, "от 5 тыс. руб.")
    await callback.message.answer("<b>от 5 тыс. руб.*</b>\n\n"
                                  "✨росписи с изображением людей на любом изделии\n"
                                  "✨шопперы с очень большими и детализированными иллюстрациями\n"
                                  "✨футболки с большими иллюстрациями/сложной идеей/детализированным фоном\n"
                                  "✨худи и свитшоты с простыми иллюстрациями от 5 тыс. / со сложными от 6.5 тыс.\n"
                                  "✨картины размером от 30 см\n\n"
                                  "* изделие входит в стоимость", reply_markup=choise_kb())
    await callback.answer()

@router.callback_query(F.data == "yes")
async def confirm_price(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(IdeaState.idea)
    await callback.message.answer("Опишите кратко идею вашего дизайна в ОДНОМ сообщении", reply_markup=back_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "other_prices")
async def other_prices(callback: CallbackQuery) -> None:
    await callback.message.edit_reply_markup(reply_markup=budget_kb())
    await callback.answer()

# Material

@router.callback_query(F.data == "shopper")
async def material_shopper(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_material_db(callback.from_user.id, "Шоппер")
    await state.set_state(DescripState.description)
    await callback.message.answer("Напишите обычный или на молнии, и желаемый цвет в ОДНОМ сообщении 🌸", reply_markup=back_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "tshirt")
async def material_tshirt(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_material_db(callback.from_user.id, "Футболка")
    await state.set_state(DescripState.description)
    await callback.message.answer("Напишите в ОДНОМ сообщении мужское/женское, цвет(можно несколько) и размер. Если сомневаетесь, можете указать примерно, я вас проконсультирую лично ☀", reply_markup=back_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "hoodie")
async def material_hoodie(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_material_db(callback.from_user.id, "Худи")
    await state.set_state(DescripState.description)
    await callback.message.answer("Напишите в ОДНОМ сообщении мужское/женское, цвет(можно несколько) и размер. Если сомневаетесь, можете указать примерно, я вас проконсультирую лично ☀", reply_markup=back_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "sweatshirt")
async def material_sweatshirt(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_material_db(callback.from_user.id, "Свитшот")
    await state.set_state(DescripState.description)
    await callback.message.answer("Напишите в ОДНОМ сообщении мужское/женское, цвет(можно несколько) и размер. Если сомневаетесь, можете указать примерно, я вас проконсультирую лично ☀", reply_markup=back_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "picture")
async def material_picture(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_material_db(callback.from_user.id, "Картина")
    await state.set_state(DescripState.description)
    await callback.message.answer("Напишите в ОДНОМ сообщении размер картины. Если сомневаетесь, можете указать примерно, я вас проконсультирую лично 🌸", reply_markup=back_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "badge")
async def material_badge(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_material_db(callback.from_user.id, "Значок")
    await state.set_state(DescripState.description)
    await callback.message.answer("Напишите в ОДНОМ сообщении каким лаком покрывать значок:\n"
                                        "<b>глянцевым</b> (цвета становятся ярче, поверхность отражающей)\n"
                                        "<b>матовым</b> (визуально никак не меняется, просто как защитный слой)\n"
                                        "либо можете написать что пока <b>не определились</b>",
                                        reply_markup=back_to_menu_kb())
    await callback.answer()

# Country

@router.callback_query(F.data == "russia")
async def russia(callback: CallbackQuery) -> None:
    await db_order.add_country_db(callback.from_user.id, "Россия")
    await callback.message.answer("Укажите способ доставки", reply_markup=russia_delivery_kb())
    await callback.answer()

@router.callback_query(F.data == "spb")
async def russia(callback: CallbackQuery) -> None:
    await db_order.add_city_db(callback.from_user.id, "Самовывоз из Санкт-Петербурга")
    row = await db_order.get_order_row(callback.from_user.id)
    if row[11] is not None:
        await callback.message.answer(f"<b>Вы выбрали следующий товар</b>\n"
                                      f"Название: {row[11]}\n"
                                      f"Цена: {row[2]}\n"
                                      f"Способ доставки: {row[8]}\n", reply_markup=confirm_order_kb())
    else:
        await callback.message.answer(f"<b>Вы выбрали следующие параметры</b>\n"
                                        f"Бюджет: {row[2]}\n"
                                        f"Идея: {row[3]}\n"
                                        f"Тип изделия: {row[4]}\n"
                                        f"Характеристики изделия: {row[5]}\n"
                                        f"Способ доставки: {row[8]}\n", reply_markup=confirm_order_kb())
    await callback.answer()

@router.callback_query(F.data == "russia_delivery")
async def russia(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_delivery_db(callback.from_user.id, "200 - 400 руб.")
    await state.set_state(CityState.city)
    await callback.message.answer("Введите адрес доставки в следующем формате:\n"
                                  "Город, улица, дом, квартира, индекс\n\n"
                                  "*отправляю Почтой России, стоимость доставки 200-400р", reply_markup=back_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "belarus")
async def belarus(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_country_db(callback.from_user.id, "Беларусь")
    await db_order.add_delivery_db(callback.from_user.id, "от 600 руб.")
    await state.set_state(CityState.city)
    await callback.message.answer("Введите адрес доставки в следующем формате:\n"
                                  "Город, улица, дом, квартира, индекс\n\n"
                                  "*отправляю Сдэком или Почтой России, стоимость доставки от 600р",
                                  reply_markup=back_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "kz")
async def kz(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_country_db(callback.from_user.id, "Казахстан")
    await db_order.add_delivery_db(callback.from_user.id, "от 600 руб.")
    await state.set_state(CityState.city)
    await callback.message.answer("Введите адрес доставки в следующем формате:\n"
                                  "Город, улица, дом, квартира, индекс\n\n"
                                  "*отправляю Сдэком или Почтой России, стоимость доставки от 600р",
                                  reply_markup=back_to_menu_kb())
    await callback.answer()

# In stock
@router.callback_query(BuyInstCF.filter())
async def buy_inst(callback: CallbackQuery, callback_data: BuyInstCF) -> None:
    scheduler = AsyncIOScheduler()
    scheduler.configure({'apscheduler.daemon': False})
    scheduler.start()
    scheduler.add_job(auto_delete_user, 'date', run_date=datetime.now() + timedelta(hours=24),
                      kwargs={'user_id': callback.from_user.id, 'username': callback.from_user.full_name})

    await db_order.create_order_table()
    await db_order.add_user_to_db(callback.from_user.id)
    await db_order.add_instock_db(callback.from_user.id, callback_data.name)
    await db_order.add_budget_db(callback.from_user.id, f"{callback_data.price} руб.")
    await callback.message.answer("В какую страну будет доставка?\n\n"
                     "*в другие страны, кроме перечисленных ниже, к сожалению, доставка невозможна",
                     reply_markup=choise_country_kb())
    await callback.answer()

# States

@router.message(IdeaState.idea)
async def user_idea(msg: Message, state: FSMContext) -> None:
    await db_order.add_idea_db(msg.from_user.id, msg.text)
    await state.clear()
    await msg.answer("Выберите изделие", reply_markup=material_kb())

@router.message(IdeaState.edit)
async def user_idea(msg: Message, state: FSMContext) -> None:
    await db_order.add_idea_db(msg.from_user.id, msg.text)
    await state.clear()
    await msg.answer("Данные успешно изменены!", reply_markup=get_data_kb())

@router.message(DescripState.description)
async def user_desc(msg: Message, state: FSMContext) -> None:
    await db_order.add_description_db(msg.from_user.id, msg.text)
    await state.clear()
    await msg.answer("В какую страну будет доставка?\n\n"
                                  "*в другие страны, кроме перечисленных ниже, к сожалению, доставка невозможна", reply_markup=choise_country_kb())

@router.message(DescripState.edit)
async def user_desc(msg: Message, state: FSMContext) -> None:
    await db_order.add_description_db(msg.from_user.id, msg.text)
    await state.clear()
    await msg.answer("Данные успешно изменены!", reply_markup=get_data_kb())

@router.message(CityState.city)
async def user_city(msg: Message, state: FSMContext) -> None:
    await db_order.add_city_db(msg.from_user.id, msg.text)
    await state.clear()
    await state.set_state(FullNameState.full_name)
    await msg.answer("Напишите ваши фамилию, имя и отчество", reply_markup=back_to_menu_kb())

@router.message(CityState.edit)
async def user_city(msg: Message, state: FSMContext) -> None:
    await db_order.add_city_db(msg.from_user.id, msg.text)
    await state.clear()
    await msg.answer("Данные успешно изменены!", reply_markup=get_data_kb())

@router.message(FullNameState.full_name)
async def user_fullname(msg: Message, state: FSMContext) -> None:
    await db_order.add_full_name_db(msg.from_user.id, msg.text)
    await state.clear()
    await state.set_state(NumberState.number)
    await msg.answer("Напишите ваш номер телефона", reply_markup=back_to_menu_kb())

@router.message(FullNameState.edit)
async def user_fullname(msg: Message, state: FSMContext) -> None:
    await db_order.add_full_name_db(msg.from_user.id, msg.text)
    await state.clear()
    await msg.answer("Данные успешно изменены!", reply_markup=get_data_kb())

@router.message(NumberState.number)
async def user_number(msg: Message, state: FSMContext) -> None:
    await db_order.add_number_db(msg.from_user.id, msg.text)
    await state.clear()
    row = await db_order.get_order_row(msg.from_user.id)
    if row[11] is not None:
        await msg.answer(f"<b>Вы выбрали следующий товар</b>\n"
                                      f"Название: {row[11]}\n"
                                      f"Цена: {row[2]}\n\n"
                         f"<b>Данные для оформления доставки</b>\n"
                                        f"ФИО: {row[6]}\n"
                                        f"Адрес: {row[7]}, {row[8]}\n"
                                        f"Номер телефона: {row[10]}\n"
                                        f"Стоимость доставки: {row[9]}", reply_markup=confirm_order_kb())
    else:
        await msg.answer(f"<b>Вы выбрали следующие параметры</b>\n"
                                        f"Бюджет: {row[2]}\n"
                                        f"Идея: {row[3]}\n"
                                        f"Тип изделия: {row[4]}\n"
                                        f"Характеристики изделия: {row[5]}\n\n"
                                        f"<b>Данные для оформления доставки</b>\n"
                                        f"ФИО: {row[6]}\n"
                                        f"Адрес: {row[7]}, {row[8]}\n"
                                        f"Номер телефона: {row[10]}\n"
                                        f"Стоимость доставки: {row[9]}", reply_markup=confirm_order_kb())

@router.message(NumberState.edit)
async def user_fullname(msg: Message, state: FSMContext) -> None:
    await db_order.add_number_db(msg.from_user.id, msg.text)
    await state.clear()
    await msg.answer("Данные успешно изменены!", reply_markup=get_data_kb())

# Send order
@router.callback_query(F.data == "send_order")
async def send_order(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(f"Спасибо, {callback.from_user.full_name}!\n"
                                  f"Заказ принят в работу🫶 Скоро я свяжусь с Вами для уточнения деталей и окончательной стоимости ☀", reply_markup=back_to_menu_kb())
    row = await db_order.get_order_row(callback.from_user.id)
    if callback.from_user.username:
        if row[6] is None and row[11] is None:
            await bot.send_message(master_id, f"<b>НОВАЯ ЗАЯВКА</b>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"Бюджет: {row[2]}\n"
                                              f"Идея: {row[3]}\n"
                                              f"Тип изделия: {row[4]}\n"
                                              f"Характеристики изделия: {row[5]}\n"
                                              f"Способ доставки: {row[8]}\n"
                                              f"Ссылка: https://t.me/{callback.from_user.username}")
        elif row[11] is not None and row[6] is None:
            await bot.send_message(master_id, f"<b>У ВАС КУПИЛИ ТОВАР В НАЛИЧИИ</b>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"Название: {row[11]}\n"
                                              f"Цена: {row[2]}\n"
                                              f"Способ доставки: {row[8]}\n"
                                              f"Ссылка: https://t.me/{callback.from_user.username}")
        elif row[11] is None and row[6] is not None:
            await bot.send_message(master_id, f"<b>НОВАЯ ЗАЯВКА</b>\n"
                                        f"Пользователь: {callback.from_user.full_name}\n"
                                        f"Бюджет: {row[2]}\n"
                                        f"Идея: {row[3]}\n"
                                        f"Тип изделия: {row[4]}\n"
                                        f"Характеристики изделия: {row[5]}\n"
                                        f"ФИО: {row[6]}\n"
                                        f"Адрес: {row[7]}, {row[8]}\n"
                                        f"Номер телефона: {row[10]}\n"
                                        f"Ссылка: https://t.me/{callback.from_user.username}")
        else:
            await bot.send_message(master_id, f"<b>У ВАС КУПИЛИ ТОВАР В НАЛИЧИИ</b>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"Название: {row[11]}\n"
                                              f"Цена: {row[2]}\n"
                                              f"ФИО: {row[6]}\n"
                                              f"Адрес: {row[7]}, {row[8]}\n"
                                              f"Номер телефона: {row[10]}\n"
                                              f"Ссылка: https://t.me/{callback.from_user.username}")
    elif not callback.from_user.username:
        if row[6] is None and row[11] is None:
            await bot.send_message(master_id, f"<b>НОВАЯ ЗАЯВКА</b>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"Бюджет: {row[2]}\n"
                                              f"Идея: {row[3]}\n"
                                              f"Тип изделия: {row[4]}\n"
                                              f"Характеристики изделия: {row[5]}\n"
                                              f"Способ доставки: {row[8]}\n"
                                              f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>")
        elif row[11] is not None:
            await bot.send_message(master_id, f"<b>У ВАС КУПИЛИ ТОВАР В НАЛИЧИИ</b>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"Название: {row[11]}\n"
                                              f"Цена: {row[2]}\n"
                                              f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>")
        elif row[11] is None and row[6] is not None:
            await bot.send_message(master_id, f"<b>НОВАЯ ЗАЯВКА</b>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"Бюджет: {row[2]}\n"
                                              f"Идея: {row[3]}\n"
                                              f"Тип изделия: {row[4]}\n"
                                              f"Характеристики изделия: {row[5]}\n"
                                              f"ФИО: {row[6]}\n"
                                              f"Адрес: {row[7]}, {row[8]}\n"
                                              f"Номер телефона: {row[10]}\n"
                                              f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>")
        else:
            await bot.send_message(master_id, f"<b>У ВАС КУПИЛИ ТОВАР В НАЛИЧИИ</b>\n"
                                              f"Пользователь: {callback.from_user.full_name}\n"
                                              f"Название: {row[11]}\n"
                                              f"Цена: {row[2]}\n"
                                              f"ФИО: {row[6]}\n"
                                              f"Адрес: {row[7]}, {row[8]}\n"
                                              f"Номер телефона: {row[10]}\n"
                                              f"У пользователя закрытый аккаунт, ваш аккаунт для связи ему отправлен, <b>ждите сообщения!</b>")
        await callback.message.answer(f"Добрый день, {callback.from_user.full_name}! Получила вашу заявку, но, кажется, у вас закрытый аккаунт и я не могу с вами связаться.\n"
                         f"Напишите мне пожалуйста в личные сообщения: {master_username}\n"
                         f"Спасибо за заказ!")
    await state.clear()
    await db_order.delete_user(callback.from_user.id)
    await callback.answer()

@router.message(F.text)
async def smthing_text(msg: Message) -> None:
    await msg.answer("Я вас не понимаю :( Воспользуйтесь, пожалуйста, кнопками или нажмите на кнопку ниже, чтобы вернуться в главное меню", reply_markup=back_to_menu_kb())


@router.message(F.photo)
async def admin_photo(msg: Message) -> None:
    if msg.from_user.id == 317325310:
        await msg.answer(msg.photo[-1].file_id)
    else:
        pass
