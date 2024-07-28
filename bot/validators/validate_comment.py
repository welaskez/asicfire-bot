from aiogram import types


def validate_comment(comment: str) -> str:
    if len(comment) >= 140:
        raise ValueError("Comment length is too long!!")
    return comment


def valid_comment_filter(message: types.Message) -> dict[str, str] | None:
    try:
        comment = validate_comment(message.text)
    except ValueError:
        return None

    return {"comment": comment}
