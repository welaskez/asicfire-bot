from utils.helpers import format_post, decode_redis_hash

from db.crud.user_requests import get_user_by_tg_id
from db.crud.post_requests import create_post

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import F, Router, types

from redis.asyncio import Redis

import config

router = Router()


@router.callback_query(F.data.startswith("publish_post:"))
async def publish_post(callback: types.CallbackQuery, r: Redis, session: AsyncSession):
    user_id = int(callback.data.split(":")[1])
    user = await get_user_by_tg_id(session=session, tg_id=user_id)

    post = decode_redis_hash(await r.hgetall(f"user:{user_id}"))

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(text="⬆️ ОПУБЛИКОВАН")
    message = await callback.message.bot.send_message(
        chat_id=config.CHANEL_USERNAME,
        text=format_post(post),
    )

    await create_post(
        session=session,
        user_id=user.id,
        name=post.get("name"),
        product=post.get("product"),
        products_count=int(post.get("products_count")),
        condition=post.get("condition"),
        price=int(post.get("price")),
        currency=post.get("currency"),
        city=post.get("city"),
        is_delivery_company=post.get("is_delivery_company"),
        comment=post.get("comment"),
        phone_number=post.get("phone_number"),
        telegram_username=post.get("telegram_username"),
        message_id=message.message_id,
    )

    await callback.message.bot.send_message(
        chat_id=int(post.get("telegram_id")),
        text="✅ Ваше объявление опубликовано",
    )
    await callback.answer()
    await r.delete(f"user:{user_id}")
