from aiogram import types


def validate_price(price: str) -> str:
    if len(price) >= 13:
        raise ValueError("Product length is too long!!")
    return price


def valid_price_filter(message: types.Message) -> dict[str, str] | None:
    try:
        price = validate_price(message.text)
    except ValueError:
        return None

    return {"price": price}
