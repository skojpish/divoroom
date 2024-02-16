from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.data_bases.content import db_content
from bot.keyboards.user_kbs import empty_inst_kb

router = Router()

class NextTenFeedbackCF(CallbackData, prefix="nextfb", sep="_"):
    starting_point: int = 0
    next_ten: bool = False

@router.callback_query(F.data == "feedback")
async def feedback_10(callback: CallbackQuery) -> None:
    reviews = []
    reviews_id = []
    reviews_next = False

    data = await db_content.get_feedback10()

    if not data:
        await callback.message.answer("Отзывы будут загружены позже, приносим свои извинения",
                                      reply_markup=empty_inst_kb())
    else:
        for row in data:
            rev_id = row[0]
            review = row[1]
            image_id = row[2]

            if image_id is None:
                reviews.append(InputMediaPhoto(type='photo', media=FSInputFile(f"django_admin/proj/media/{review}")))
            else:
                reviews.append(InputMediaPhoto(type='photo', media=f'{image_id}'))

            reviews_id.append(rev_id)

        if await db_content.get_feedback_more(10):
            reviews_next = True

        def feedback_kb() -> InlineKeyboardMarkup:
            kb = InlineKeyboardBuilder()
            kb.add(InlineKeyboardButton(
                text="Заказать собственный дизайн", callback_data="order"
            ))
            if reviews_next:
                kb.button(
                    text=f"Посмотреть еще", callback_data=NextTenFeedbackCF(next_ten=True, starting_point=10)
                )
            kb.add(InlineKeyboardButton(
                text="Вернуться в главное меню", callback_data="back_to_menu"
            ))
            kb.adjust(1)
            return kb.as_markup()

        media_gr = await callback.message.answer_media_group(reviews)

        for row in data:
            rev_id = row[0]
            image_id = row[2]

            if image_id is None:
                image_id_cur = media_gr[data.index(row)].photo[-1].file_id
                await db_content.add_image_id(rev_id, image_id_cur)

        await callback.message.answer("Отзывы", reply_markup=feedback_kb())

    await callback.answer()

@router.callback_query(NextTenFeedbackCF.filter(F.next_ten==True))
async def feedback_more(callback: CallbackQuery, callback_data: NextTenFeedbackCF) -> None:
    reviews = []
    reviews_id = []
    reviews_next = False

    data = await db_content.get_feedback_more(callback_data.starting_point)

    for row in data:
        rev_id = row[0]
        review = row[1]
        image_id = row[2]

        if image_id is None:
            reviews.append(InputMediaPhoto(type='photo', media=FSInputFile(f"django_admin/proj/media/{review}")))
        else:
            reviews.append(InputMediaPhoto(type='photo', media=f'{image_id}'))

        reviews_id.append(rev_id)

    if await db_content.get_feedback_more(callback_data.starting_point+10):
        reviews_next = True

    def feedback_kb() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(InlineKeyboardButton(
            text="Заказать собственный дизайн", callback_data="order"
        ))
        if reviews_next:
            kb.button(
                text=f"Посмотреть еще", callback_data=NextTenFeedbackCF(next_ten=True,
                                                                        starting_point=callback_data.starting_point+10)
            )
        kb.add(InlineKeyboardButton(
            text="Вернуться в главное меню", callback_data="back_to_menu"
        ))
        kb.adjust(1)
        return kb.as_markup()

    media_gr = await callback.message.answer_media_group(reviews)

    for row in data:
        rev_id = row[0]
        image_id = row[2]

        if image_id is None:
            image_id_cur = media_gr[data.index(row)].photo[-1].file_id
            await db_content.add_image_id(rev_id, image_id_cur)

    await callback.message.answer("Отзывы", reply_markup=feedback_kb())

    await callback.answer()
