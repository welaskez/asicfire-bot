from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    name = State()
    product = State()
    products_count = State()
    condition = State()
    price = State()
    currency = State()
    city = State()
    is_delivery_company = State()
    phone_number = State()
    telegram_username = State()
    comment = State()
