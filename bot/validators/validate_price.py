from aiogram import types

import re


def validate_price(price: str) -> str:
    price = price.strip().replace(",", ".")

    if not re.match(r"^\d+(\.\d{1,2})?$", price):
        raise ValueError("Invalid price format. Please enter a valid number.")

    price_int = int(price)

    if price_int <= 0:
        raise ValueError("Price must be a positive number.")

    if price_int >= 1e12:
        raise ValueError("Price is too high.")

    return price


def valid_price_filter(message: types.Message) -> dict[str, str] | None:
    try:
        price = validate_price(message.text)
    except ValueError:
        return None

    return {"price": price}
