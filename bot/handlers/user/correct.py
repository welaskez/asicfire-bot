from keyboards.inline import inline_keyboard, inline_button

from aiogram.fsm.context import FSMContext
from aiogram import F, Router, types

from redis.asyncio import Redis

from utils.helpers import format_post
from utils.messages import end

import config

router = Router()


@router.callback_query(F.data == "correct")
async def send_post_to_admin(
    callback: types.CallbackQuery,
    state: FSMContext,
    r: Redis,
):
    post = await state.get_data()
    await state.clear()
    await r.hmset(name=f"user:{callback.from_user.id}", mapping=post)

    await callback.message.answer(
        text=end,
        reply_markup=inline_keyboard(
            buttons=[inline_button(text="Продолжить", callback_data="next")]
        ),
    )
    await callback.answer()

    await callback.message.bot.send_message(
        chat_id=config.ADMINS[0],
        text="Новый пост!\n" + format_post(post=post),
        reply_markup=inline_keyboard(
            buttons=[
                inline_button(
                    text="Опубликовать",
                    callback_data=f"publish_post:{callback.from_user.id}",
                ),
                inline_button(
                    text="Не опубликовывать",
                    callback_data=f"dont_publish_post:{callback.from_user.id}",
                ),
            ]
        ),
    )

    await callback.answer()
