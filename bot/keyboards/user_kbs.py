from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.data_bases.order import db_order


def start_kb() -> InlineKeyboardMarkup:
    """Get kb for start menu
    """
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Заказать собственный дизайн", callback_data="order"
    ))
    kb.add(InlineKeyboardButton(
        text="Работы в наличии", callback_data="instock"
    ))
    kb.add(InlineKeyboardButton(
        text="Примеры работ", callback_data="examples"
    ))
    kb.add(InlineKeyboardButton(
        text="Отзывы", callback_data="feedback"
    ))
    kb.add(InlineKeyboardButton(
        text="Обо мне", callback_data="about"
    ))
    kb.adjust(1)
    return kb.as_markup()

def examples_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Шопперы", callback_data="shoppers_ex"
    ))
    kb.add(InlineKeyboardButton(
        text="Футболки", callback_data="tshirts_ex"
    ))
    kb.add(InlineKeyboardButton(
        text="Худи/свитшоты", callback_data="hoodies_sweat_ex"
    ))
    kb.add(InlineKeyboardButton(
        text="Картины", callback_data="pictures_ex"
    ))
    kb.add(InlineKeyboardButton(
        text="Значки", callback_data="badges_ex"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def ex_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Заказать собственный дизайн", callback_data="order"
    ))
    kb.add(InlineKeyboardButton(
        text="Посмотреть другие категории", callback_data="other_cat"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def about_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Заказать собственный дизайн", callback_data="order"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def back_to_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def back2_to_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Назад", callback_data="back"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def budget_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="1.5 - 3.5 тыс. руб.", callback_data="sum_13"
    ))
    kb.add(InlineKeyboardButton(
        text="3.5 - 5 тыс. руб.", callback_data="sum_35"
    ))
    kb.add(InlineKeyboardButton(
        text="от 5 тыс. руб.", callback_data="sum_5"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def choise_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Да, устраивает", callback_data="yes"
    ))
    kb.add(InlineKeyboardButton(
        text="Посмотреть варианты с другими ценами", callback_data="other_prices"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def material_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Шоппер", callback_data="shopper"
    ))
    kb.add(InlineKeyboardButton(
        text="Футболка", callback_data="tshirt"
    ))
    kb.add(InlineKeyboardButton(
        text="Свитшот", callback_data="sweatshirt"
    ))
    kb.add(InlineKeyboardButton(
        text="Худи", callback_data="hoodie"
    ))
    kb.add(InlineKeyboardButton(
        text="Картина", callback_data="picture"
    ))
    kb.add(InlineKeyboardButton(
        text="Значок", callback_data="badge"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def choise_country_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Россия", callback_data="russia"
    ))
    kb.add(InlineKeyboardButton(
        text="Беларусь", callback_data="belarus"
    ))
    kb.add(InlineKeyboardButton(
        text="Казахстан", callback_data="kz"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def russia_delivery_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Забрать самовывозом из Санкт-Петербурга", callback_data="spb"
    ))
    kb.add(InlineKeyboardButton(
        text="Заказать доставку в другой город России", callback_data="russia_delivery"
    ))
    kb.add(InlineKeyboardButton(
        text="Назад", callback_data="back"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def confirm_order_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Отправить заявку", callback_data="send_order"
    ))
    kb.add(InlineKeyboardButton(
        text="Отредактировать данные", callback_data="edit_order"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def empty_inst_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Заказать собственный дизайн", callback_data="order"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

async def edit_order_kb(user) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    row = await db_order.get_order_row(user)
    if row[6] is None and row[11] is None:
        kb.add(InlineKeyboardButton(
            text="Бюджет", callback_data="budget_edit"
        ))
        kb.add(InlineKeyboardButton(
            text="Идея", callback_data="idea_edit"
        ))
        kb.add(InlineKeyboardButton(
            text="Тип изделия", callback_data="material_edit"
        ))
        kb.add(InlineKeyboardButton(
            text="Характеристики изделия", callback_data="description_edit"
        ))
        kb.add(InlineKeyboardButton(
            text="Способ доставки", callback_data="country_edit"
        ))
    elif row[11] is not None and row[6] is None:
        kb.add(InlineKeyboardButton(
            text="Способ доставки", callback_data="country_edit"
        ))
    elif row[11] is None and row[6] is not None:
        kb.add(InlineKeyboardButton(
            text="Параметры изделия", callback_data="param_edit"
        ))
        kb.add(InlineKeyboardButton(
            text="Данные о доставке", callback_data="delivery_edit"
        ))
    else:
        kb.add(InlineKeyboardButton(
            text="ФИО", callback_data="fullname_edit"
        ))
        kb.add(InlineKeyboardButton(
            text="Адрес", callback_data="country_edit"
        ))
        kb.add(InlineKeyboardButton(
            text="Номер телефона", callback_data="number_edit"
        ))
    kb.add(InlineKeyboardButton(
        text="Назад", callback_data="back"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def edit_order_param_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Бюджет", callback_data="budget_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Идея", callback_data="idea_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Тип изделия", callback_data="material_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Характеристики изделия", callback_data="description_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Назад", callback_data="edit_order"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def edit_order_delivery_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="ФИО", callback_data="fullname_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Адрес", callback_data="country_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Номер телефона", callback_data="number_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Назад", callback_data="edit_order"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def auto_delete_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Составить новую заявку", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()
