from aiogram import F, Router, types

from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.user_requests import get_user_by_tg_id, create_user

from utils.messages import ecosystem_poolproof_text

from keyboards.inline import inline_keyboard, inline_button

router = Router()


@router.callback_query(F.data == "ecosystem_poolproof")
async def ecosystem_poolproof(callback: types.CallbackQuery, session: AsyncSession):
    user = await get_user_by_tg_id(session=session, tg_id=callback.from_user.id)
    if not user:
        await create_user(
            session=session,
            tg_id=callback.from_user.id,
            wallet_address=str(callback.from_user.id),
        )

    await callback.message.answer(
        text=ecosystem_poolproof_text,
        reply_markup=inline_keyboard(
            buttons=[
                inline_button(text="POOLPROOF | BOT", url="https://t.me/poolproofbot"),
                inline_button(text="THE MINERS CLUB", url="https://t.me/theminersclub"),
                inline_button(text="POOLPROOF", url="https://t.me/poolproof"),
                inline_button(text="Журнал майнера", url="https://t.me/poolprooftech"),
                inline_button(text="AsicFire", url="https://t.me/asicfire"),
                inline_button(text="Service", callback_data="nothing"),
                inline_button(text="Продолжить", callback_data="faq"),
            ],
            adjust=(
                1,
                1,
                2,
                2,
                1,
            ),
        ),
    )
    await callback.answer()
