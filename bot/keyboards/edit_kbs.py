from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def edit_budget_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="1 - 3.5 тыс. руб.", callback_data="sum_13_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="3.5 - 5 тыс. руб.", callback_data="sum_35_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="от 5 тыс. руб.", callback_data="sum_5_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Назад", callback_data="back"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def edit_choise_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Да, устраивает", callback_data="yes_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Посмотреть варианты с другими ценами", callback_data="other_prices_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Назад", callback_data="back"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def get_data_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Перейти к заявке", callback_data="go_to_order"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def material_edit_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Шоппер", callback_data="shopper_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Футболка", callback_data="tshirt_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Свитшот", callback_data="sweatshirt_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Худи", callback_data="hoodie_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Картина", callback_data="picture_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Значок", callback_data="badge_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Назад", callback_data="back"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def edit_country_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Россия", callback_data="russia_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Беларусь", callback_data="belarus_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Казахстан", callback_data="kz_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Назад", callback_data="back"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()

def edit_russia_delivery_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Забрать самовывозом из Санкт-Петербурга", callback_data="spb_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Заказать доставку в другой город России", callback_data="russia_delivery_edit"
    ))
    kb.add(InlineKeyboardButton(
        text="Назад", callback_data="back"
    ))
    kb.add(InlineKeyboardButton(
        text="Вернуться в главное меню", callback_data="back_to_menu"
    ))
    kb.adjust(1)
    return kb.as_markup()