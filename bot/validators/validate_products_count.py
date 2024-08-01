from aiogram import types

import re


def validate_products_count(products_count: str) -> str:
    products_count = products_count.strip()

    if not re.match(r"^\d+$", products_count):
        raise ValueError("Invalid product count. Please enter a positive whole number.")

    count = int(products_count)

    if count <= 0:
        raise ValueError("Product count must be a positive number.")

    if count > 99999:
        raise ValueError("Product count is too high. Maximum allowed is 99999.")

    return products_count


def valid_products_count_filter(message: types.Message) -> dict[str, str] | None:
    try:
        products_count = validate_products_count(message.text)
    except ValueError:
        return None

    return {"products_count": products_count}
