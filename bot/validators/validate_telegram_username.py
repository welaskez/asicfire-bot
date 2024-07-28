from aiogram import types


def validate_telegram_username(telegram_username: str) -> str:
    if len(telegram_username) >= 32:
        raise ValueError("Product length is too long!!")
    return telegram_username


def valid_telegram_username_filter(message: types.Message) -> dict[str, str] | None:
    try:
        telegram_username = validate_telegram_username(message.text)
    except ValueError:
        return None

    return {
        "telegram_username": (
            "@" + telegram_username
            if telegram_username[0] != "@"
            else telegram_username
        )
    }
