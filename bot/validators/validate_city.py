from aiogram import types


def validate_city(city: str) -> str | None:
    if len(city) >= 25:
        raise ValueError("City length is too long!")
    return city


def valid_city_filter(message: types.Message) -> dict[str, str] | None:
    try:
        city = validate_city(message.text)
    except ValueError:
        return None

    return {"city": city}
