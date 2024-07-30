from datetime import datetime, timezone
from types import NoneType

from db.models import User

from .messages import post_template


def format_post(post: dict) -> str:
    return post_template.format(
        post.get("name"),
        post.get("product"),
        post.get("products_count"),
        post.get("condition"),
        post.get("price"),
        "$" if post.get("currency") == "РУБ" else "₽",
        post.get("city"),
        post.get("is_delivery_company"),
        post.get("comment"),
        post.get("phone_number"),
        post.get("telegram_username"),
    )


def decode_redis_hash(hash_data: dict) -> dict:
    return {k.decode("utf-8"): v.decode("utf-8") for k, v in hash_data.items()}


def is_post_limit_expired(user: User) -> bool:
    if user.post_limits_expiration_time is None:
        return False

    now = datetime.now(timezone.utc)
    expiration_time = user.post_limits_expiration_time

    if expiration_time.tzinfo is None:
        expiration_time = expiration_time.replace(tzinfo=timezone.utc)

    return now > expiration_time
