from aiogram import types


def validate_phone_number(phone_number: str) -> str | None:
    if len(phone_number) > 16 or len(phone_number) < 10:
        raise ValueError("Phone number invalid")
    return phone_number


def valid_phone_number_filter(message: types.Message) -> dict[str, str] | None:
    try:
        phone_number = validate_phone_number(message.text)
    except ValueError:
        return None

    return {"phone_number": phone_number}
