from datetime import datetime, timezone

from .messages import post_template


def is_post_limit_expired(expiration_time: datetime | None) -> bool:
    return (
        expiration_time < datetime.now(timezone.utc)
        if expiration_time is not None
        else True
    )


def calculate_time_left(expiration_time: datetime) -> str:
    time_left = expiration_time - datetime.now(timezone.utc)
    hours = time_left.seconds // 3600
    minutes = (time_left.seconds % 3600) // 60
    seconds = time_left.seconds % 60

    return f"{hours} часов {minutes} минут {seconds} секунд"


def format_post(post: dict) -> str:
    return post_template.format(
        post.get("name"),
        post.get("product"),
        post.get("products_count"),
        post.get("condition"),
        post.get("price"),
        "₽" if post.get("currency") == "РУБ" else "$",
        post.get("city"),
        post.get("is_delivery_company"),
        post.get("comment"),
        post.get("phone_number"),
        post.get("telegram_username"),
    )


def decode_redis_hash(hash_data: dict) -> dict:
    return {k.decode("utf-8"): v.decode("utf-8") for k, v in hash_data.items()}
