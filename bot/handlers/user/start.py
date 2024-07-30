from aiogram import Router, types
from aiogram.filters import Command

from keyboards.inline import inline_keyboard, inline_button

from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.user_requests import get_user_by_tg_id, create_user

from utils.messages import start

from config import BASE_DIR

router = Router()


@router.message(Command("start"))
async def newsletter_cmd(message: types.Message, session: AsyncSession):
    user = await get_user_by_tg_id(session=session, tg_id=message.from_user.id)
    if user:
        pass
    if not user:
        await create_user(
            session=session,
            tg_id=message.from_user.id,
            wallet_address=str(message.from_user.id),
        )
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
