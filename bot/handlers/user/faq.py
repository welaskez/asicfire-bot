from aiogram import F, Router, types

from keyboards.inline import inline_keyboard, inline_button
from utils.messages import faq_text

router = Router()


@router.callback_query(F.data == "faq")
async def faq(callback: types.CallbackQuery):
    await callback.message.answer(
        text=faq_text,
        reply_markup=inline_keyboard(
            buttons=[
                inline_button(
                    text="Опубликовать объявление", callback_data="sell_asic"
                ),
            ]
        ),
    )
