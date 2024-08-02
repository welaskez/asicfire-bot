from db.crud.user_requests import get_user_by_tg_id, create_user

from keyboards.inline import inline_keyboard, inline_button

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import F, Router, types

import config

router = Router()


@router.callback_query(F.data == "next")
async def next_cmd(callback: types.CallbackQuery, session: AsyncSession):
    user = await get_user_by_tg_id(session=session, tg_id=callback.from_user.id)
    if not user:
        await create_user(
            session=session,
            tg_id=callback.from_user.id,
            wallet_address=str(callback.from_user.id),
        )

    await callback.message.answer_photo(
        photo=types.FSInputFile(f"{config.BASE_DIR}/imgs/img.jpg"),
        caption="📲 Если вам требуется срочно продать устройство - заполните объявление, и мы "
        "разместим его в удобном формате\n\nУзнать информацию о продавце - @asicfirechat",
        reply_markup=inline_keyboard(
            buttons=[
                inline_button(text="Продать устройство", callback_data="sell_asic"),
                inline_button(
                    text="Экосистема poolproof", callback_data="ecosystem_poolproof"
                ),
            ]
        ),
    )
    await callback.answer()
