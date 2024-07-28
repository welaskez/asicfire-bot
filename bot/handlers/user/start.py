from aiogram import Router, types
from aiogram.filters import Command

from keyboards.inline import inline_keyboard, inline_button

from utils.messages import start

from config import BASE_DIR

router = Router()


@router.message(Command("start"))
async def newsletter_cmd(message: types.Message):
    await message.answer_photo(
        photo=types.FSInputFile(f"{BASE_DIR}/imgs/img.jpg"),
        caption=start,
        reply_markup=inline_keyboard(
            buttons=[
                inline_button(text="Продать устройство", callback_data="faq"),
                inline_button(
                    text="Экосистема poolproof", callback_data="ecosystem_poolproof"
                ),
            ]
        ),
    )
