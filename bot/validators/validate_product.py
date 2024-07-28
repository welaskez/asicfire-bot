from aiogram import types


def validate_product(product: str) -> str:
    if len(product) >= 35:
        raise ValueError("Product length is too long!!")
    return product


def valid_product_filter(message: types.Message) -> dict[str, str] | None:
    try:
        product = validate_product(message.text)
    except ValueError:
        return None

    return {"product": product}
