from utils.helpers import decode_redis_hash

from aiogram import F, Router, types

from redis.asyncio import Redis

router = Router()


@router.callback_query(F.data.startswith("dont_publish_post:"))
async def dont_publish_post(callback: types.CallbackQuery, r: Redis):
    user_id = int(callback.data.split(":")[1])
    post = decode_redis_hash(await r.hgetall(f"user:{user_id}"))

    await callback.message.answer("⬆️ НЕ ОПУБЛИКОВАН")
    await callback.message.bot.send_message(
        chat_id=int(post.get("telegram_id")),
        text="🚫 Ваш пост не прошел проверку\n\nСвяжитесь с @asicfire_admin",
    )
    await callback.answer()
    await r.delete(f"user:{user_id}")
