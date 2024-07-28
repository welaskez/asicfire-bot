from aiogram import types


def validate_products_count(products_count: str) -> str:
    if len(products_count) > 5:
        raise ValueError("Products count length is too long!!")
    return products_count


def valid_products_count_filter(message: types.Message) -> dict[str, str] | None:
    try:
        products_count = validate_products_count(message.text)
    except ValueError:
        return None

    return {"products_count": products_count}
