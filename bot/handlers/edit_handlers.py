from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.data_bases.fsm import IdeaState, DescripState, CityState, FullNameState, NumberState
from bot.data_bases.order import db_order

from bot.keyboards.edit_kbs import edit_budget_kb, edit_choise_kb, get_data_kb, material_edit_kb, edit_country_kb, \
    edit_russia_delivery_kb
from bot.keyboards.user_kbs import confirm_order_kb, back2_to_menu_kb, edit_order_delivery_kb, edit_order_param_kb, \
    edit_order_kb

router = Router()

# Edit order
@router.callback_query(F.data == "edit_order")
async def edit_order(callback: CallbackQuery) -> None:
    row = await db_order.get_order_row(callback.from_user.id)
    if row[11] is None and row[6] is not None:
        await callback.message.answer("Выберите параметры, которые вы хотели бы изменить",
                                      reply_markup=await edit_order_kb(callback.from_user.id))
    else:
        await callback.message.answer("Выберите параметр, который вы хотели бы изменить",
                     reply_markup=await edit_order_kb(callback.from_user.id))
    await callback.answer()

@router.callback_query(F.data == "param_edit")
async def edit_order(callback: CallbackQuery) -> None:
    await callback.message.delete()
    await callback.message.answer("Выберите параметр, который вы хотели бы изменить",
                     reply_markup=edit_order_param_kb())
    await callback.answer()

@router.callback_query(F.data == "delivery_edit")
async def edit_order(callback: CallbackQuery) -> None:
    await callback.message.delete()
    await callback.message.answer("Выберите параметр, который вы хотели бы изменить",
                     reply_markup=edit_order_delivery_kb())
    await callback.answer()

# Edit budget
@router.callback_query(F.data == "budget_edit")
async def edit_budget(callback: CallbackQuery) -> None:
    await callback.message.answer("Какой ваш примерный бюджет?", reply_markup=edit_budget_kb())
    await callback.answer()

@router.callback_query(F.data == "sum_13_edit")
async def price_13_edit(callback: CallbackQuery) -> None:
    await db_order.add_budget_db(callback.from_user.id, "1.5 - 3.5 тыс. руб.")
    await callback.message.answer("<b>1.5 - 3.5 тыс. руб.*</b>\n\n"
                                  "✨любые значки 1.5 тыс.\n"
                                  "✨шопперы с надписями/маленькими простыми иллюстрациями 2 - 3.5 тыс.\n\n"
                                  "* изделие входит в стоимость", reply_markup=edit_choise_kb())
    await callback.answer()

@router.callback_query(F.data == "sum_35_edit")
async def price_35_edit(callback: CallbackQuery) -> None:
    await db_order.add_budget_db(callback.from_user.id, "3.5 - 5 тыс. руб.")
    await callback.message.answer("<b>3.5 - 5 тыс. руб.*</b>\n\n"
                                  "✨шопперы с иллюстрациями животных(одного), без фона, от 3.5 тыс\n"
                                  "✨шопперы с иллюстрациями животных(2 и больше), без фона, от 4 тыс \n"
                                  "✨шопперы с животными с фоном, от 4 тыс\n"
                                  "✨футболки с иллюстрациями 1-2 животных, ~5 тыс\n"
                                  "✨картины размером ~20х20 см, с однотонным фоном\n\n"
                                  "🐥все иллюстрации на другую тематику рассчитываются в "
                                  "зависимости от сложности, выбирайте просто по своему бюджету(также см. раздел «от 5тыс.»)\n\n"
                                  "* изделие входит в стоимость", reply_markup=edit_choise_kb())
    await callback.answer()

@router.callback_query(F.data == "sum_5_edit")
async def price_5_edit(callback: CallbackQuery) -> None:
    await db_order.add_budget_db(callback.from_user.id, "от 5 тыс. руб.")
    await callback.message.answer("<b>от 5 тыс. руб.*</b>\n\n"
                                  "✨росписи с изображением людей на любом изделии\n"
                                  "✨шопперы с очень большими и детализированными иллюстрациями\n"
                                  "✨футболки с большими иллюстрациями/сложной идеей/детализированным фоном\n"
                                  "✨худи и свитшоты с простыми иллюстрациями от 5 тыс. / со сложными от 6.5 тыс.\n"
                                  "✨картины размером от 30 см\n\n"
                                  "* изделие входит в стоимость", reply_markup=edit_choise_kb())
    await callback.answer()

@router.callback_query(F.data == "yes_edit")
async def confirm_price_edit(callback: CallbackQuery) -> None:
    await callback.message.answer("Данные успешно изменены!", reply_markup=get_data_kb())
    await callback.answer()

@router.callback_query(F.data == "other_prices_edit")
async def other_prices_edit(callback: CallbackQuery) -> None:
    await callback.message.edit_reply_markup(reply_markup=edit_budget_kb())
    await callback.answer()

@router.callback_query(F.data == "go_to_order")
async def other_prices(callback: CallbackQuery) -> None:
    row = await db_order.get_order_row(callback.from_user.id)
    if row[11] is not None and row[6] is None:
        await callback.message.answer(f"<b>Вы выбрали следующий товар</b>\n"
                                      f"Название: {row[11]}\n"
                                      f"Цена: {row[2]}\n"
                                      f"Способ доставки: {row[8]}\n", reply_markup=confirm_order_kb())
    elif row[6] is None and row[11] is None:
        await callback.message.answer(f"<b>Вы выбрали следующие параметры</b>\n"
                                      f"Бюджет: {row[2]}\n"
                                      f"Идея: {row[3]}\n"
                                      f"Тип изделия: {row[4]}\n"
                                      f"Характеристики изделия: {row[5]}\n"
                                      f"Способ доставки: {row[8]}\n", reply_markup=confirm_order_kb())
    elif row[11] is None and row[6] is not None:
        await callback.message.answer(f"<b>Вы выбрали следующие параметры</b>\n"
                                        f"Бюджет: {row[2]}\n"
                                        f"Идея: {row[3]}\n"
                                        f"Тип изделия: {row[4]}\n"
                                        f"Характеристики изделия: {row[5]}\n\n"
                                        f"<b>Данные для оформления доставки</b>\n"
                                        f"ФИО: {row[6]}\n"
                                        f"Адрес: {row[7]}, {row[8]}\n"
                                        f"Номер телефона: {row[10]}\n"
                                        f"Стоимость доставки: {row[9]}", reply_markup=confirm_order_kb())
    else:
        await callback.message.answer(f"<b>Вы выбрали следующий товар</b>\n"
                                      f"Название: {row[11]}\n"
                                      f"Цена: {row[2]}\n\n"
                         f"<b>Данные для оформления доставки</b>\n"
                                        f"ФИО: {row[6]}\n"
                                        f"Адрес: {row[7]}, {row[8]}\n"
                                        f"Номер телефона: {row[10]}\n"
                                        f"Стоимость доставки: {row[9]}", reply_markup=confirm_order_kb())
    await callback.answer()

# Edit idea
@router.callback_query(F.data == "idea_edit")
async def edit_budget(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(IdeaState.edit)
    await callback.message.answer("Опишите кратко идею вашего дизайна в ОДНОМ сообщении",
                                  reply_markup=back2_to_menu_kb())
    await callback.answer()

# Edit material
@router.callback_query(F.data == "material_edit")
async def edit_budget(callback: CallbackQuery) -> None:
    await callback.message.answer("Выберите изделие", reply_markup=material_edit_kb())
    await callback.answer()

@router.callback_query(F.data == "shopper_edit")
async def material_shopper(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_material_db(callback.from_user.id, "Шоппер")
    await state.set_state(DescripState.edit)
    await callback.message.answer("Напишите обычный или на молнии, и желаемый цвет в ОДНОМ сообщении 🌸", reply_markup=back2_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "tshirt_edit")
async def material_tshirt(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_material_db(callback.from_user.id, "Футболка")
    await state.set_state(DescripState.edit)
    await callback.message.answer("Напишите в ОДНОМ сообщении мужское/женское, цвет(можно несколько) и размер. Если сомневаетесь, можете указать примерно, я вас проконсультирую лично ☀", reply_markup=back2_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "hoodie_edit")
async def material_hoodie(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_material_db(callback.from_user.id, "Худи")
    await state.set_state(DescripState.edit)
    await callback.message.answer("Напишите в ОДНОМ сообщении мужское/женское, цвет(можно несколько) и размер. Если сомневаетесь, можете указать примерно, я вас проконсультирую лично ☀", reply_markup=back2_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "sweatshirt_edit")
async def material_sweatshirt(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_material_db(callback.from_user.id, "Свитшот")
    await state.set_state(DescripState.edit)
    await callback.message.answer("Напишите в ОДНОМ сообщении мужское/женское, цвет(можно несколько) и размер. Если сомневаетесь, можете указать примерно, я вас проконсультирую лично ☀", reply_markup=back2_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "picture_edit")
async def material_picture(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_material_db(callback.from_user.id, "Картина")
    await state.set_state(DescripState.edit)
    await callback.message.answer("Напишите в ОДНОМ сообщении размер картины. Если сомневаетесь, можете указать примерно, я вас проконсультирую лично 🌸", reply_markup=back2_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "badge_edit")
async def material_badge(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_material_db(callback.from_user.id, "Значок")
    await state.set_state(DescripState.edit)
    await callback.message.answer("Напишите в ОДНОМ сообщении каким лаком покрывать значок:\n"
                                        "<b>глянцевым</b> (цвета становятся ярче, поверхность отражающей)\n"
                                        "<b>матовым</b> (визуально никак не меняется, просто как защитный слой)\n"
                                        "либо можете написать что пока <b>не определились</b>",
                                        reply_markup=back2_to_menu_kb())
    await callback.answer()

# Desc edit
@router.callback_query(F.data == "description_edit")
async def edit_budget(callback: CallbackQuery, state: FSMContext) -> None:
    row = await db_order.get_order_row(callback.from_user.id)
    if row[4] == "Шоппер":
        await db_order.add_material_db(callback.from_user.id, "Шоппер")
        await state.set_state(DescripState.edit)
        await callback.message.answer("Напишите обычный или на молнии, и желаемый цвет в ОДНОМ сообщении 🌸",
                                            reply_markup=back2_to_menu_kb())
    elif row[4] == "Футболка":
        await db_order.add_material_db(callback.from_user.id, "Футболка")
        await state.set_state(DescripState.edit)
        await callback.message.answer("Напишите в ОДНОМ сообщении мужское/женское, цвет(можно несколько) и размер. Если сомневаетесь, можете указать примерно, я вас проконсультирую лично ☀",
                                            reply_markup=back2_to_menu_kb())
    elif row[4] == "Свитшот":
        await db_order.add_material_db(callback.from_user.id, "Свитшот")
        await state.set_state(DescripState.edit)
        await callback.message.answer("Напишите в ОДНОМ сообщении мужское/женское, цвет(можно несколько) и размер. Если сомневаетесь, можете указать примерно, я вас проконсультирую лично ☀",
                                            reply_markup=back2_to_menu_kb())
    elif row[4] == "Худи":
        await db_order.add_material_db(callback.from_user.id, "Худи")
        await state.set_state(DescripState.edit)
        await callback.message.answer("Напишите в ОДНОМ сообщении мужское/женское, цвет(можно несколько) и размер. Если сомневаетесь, можете указать примерно, я вас проконсультирую лично ☀",
                                            reply_markup=back2_to_menu_kb())
    elif row[4] == "Картина":
        await db_order.add_material_db(callback.from_user.id, "Картина")
        await state.set_state(DescripState.edit)
        await callback.message.answer("Напишите в ОДНОМ сообщении размер картины. Если сомневаетесь, можете указать примерно, я вас проконсультирую лично 🌸",
                                            reply_markup=back2_to_menu_kb())
    elif row[4] == "Значок":
        await db_order.add_material_db(callback.from_user.id, "Значок")
        await state.set_state(DescripState.edit)
        await callback.message.answer("Напишите в ОДНОМ сообщении каким лаком покрывать значок:\n"
                                            "<b>глянцевым</b> (цвета становятся ярче, поверхность отражающей)\n"
                                            "<b>матовым</b> (визуально никак не меняется, просто как защитный слой)\n"
                                            "либо можете написать что пока <b>не определились</b>",
                                            reply_markup=back2_to_menu_kb())
    await callback.answer()

# Country edit
@router.callback_query(F.data == "country_edit")
async def edit_country(callback: CallbackQuery) -> None:
    await callback.message.answer("В какую страну будет доставка?\n\n"
                     "*в другие страны, кроме перечисленных ниже, к сожалению, доставка невозможна",
                     reply_markup=edit_country_kb())
    await callback.answer()

@router.callback_query(F.data == "russia_edit")
async def russia(callback: CallbackQuery) -> None:
    await db_order.add_country_db(callback.from_user.id, "Россия")
    await callback.message.answer("Укажите способ доставки", reply_markup=edit_russia_delivery_kb())
    await callback.answer()

@router.callback_query(F.data == "spb_edit")
async def russia(callback: CallbackQuery) -> None:
    await db_order.add_city_db(callback.from_user.id, "Самовывоз из Санкт-Петербурга")
    await callback.message.answer("Данные успешно изменены!", reply_markup=get_data_kb())
    await callback.answer()

@router.callback_query(F.data == "russia_delivery_edit")
async def russia(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_delivery_db(callback.from_user.id, "200 - 400 руб.")
    await state.set_state(CityState.edit)
    await callback.message.answer("Введите адрес доставки в следующем формате:\n"
                                  "Город, улица, дом, квартира, индекс\n\n"
                                  "*отправляю Почтой России, стоимость доставки 200-400р", reply_markup=back2_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "belarus_edit")
async def belarus(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_country_db(callback.from_user.id, "Беларусь")
    await db_order.add_delivery_db(callback.from_user.id, "от 600 руб.")
    await state.set_state(CityState.edit)
    await callback.message.answer("Введите адрес доставки в следующем формате:\n"
                                  "Город, улица, дом, квартира, индекс\n\n"
                                  "*отправляю Сдэком или Почтой России, стоимость доставки от 600р",
                                  reply_markup=back2_to_menu_kb())
    await callback.answer()

@router.callback_query(F.data == "kz_edit")
async def kz(callback: CallbackQuery, state: FSMContext) -> None:
    await db_order.add_country_db(callback.from_user.id, "Казахстан")
    await db_order.add_delivery_db(callback.from_user.id, "от 600 руб.")
    await state.set_state(CityState.edit)
    await callback.message.answer("Введите адрес доставки в следующем формате:\n"
                                  "Город, улица, дом, квартира, индекс\n\n"
                                  "*отправляю Сдэком или Почтой России, стоимость доставки от 600р",
                                  reply_markup=back2_to_menu_kb())
    await callback.answer()

# Fullname edit
@router.callback_query(F.data == "fullname_edit")
async def edit_fullname(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FullNameState.edit)
    await callback.message.answer("Напишите ваши фамилию, имя и отчество", reply_markup=back2_to_menu_kb())
    await callback.answer()

# Number edit
@router.callback_query(F.data == "number_edit")
async def edit_fullname(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(NumberState.edit)
    await callback.message.answer("Напишите ваш номер телефона", reply_markup=back2_to_menu_kb())
    await callback.answer()
