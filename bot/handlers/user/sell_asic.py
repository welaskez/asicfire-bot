from keyboards.inline import inline_keyboard, inline_button

from datetime import datetime, timedelta, timezone

from db.crud.user_requests import get_user_by_tg_id, update_user

from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.fsm.context import FSMContext
from aiogram import F, Router, types

from validators import (
    valid_products_count_filter,
    valid_phone_number_filter,
    valid_city_filter,
    valid_comment_filter,
    valid_product_filter,
    valid_price_filter,
    valid_telegram_username_filter,
)

from utils.messages import sell_asic_msgs, sell_asic_error_msgs, post_limit_message
from utils.helpers import format_post, is_post_limit_expired, calculate_time_left

from states import UserState

router = Router()


@router.callback_query(F.data == "sell_asic")
async def sell_asic_cmd(
    callback: types.CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    user = await get_user_by_tg_id(session=session, tg_id=callback.from_user.id)

    if user.post_limits_expiration_time is None or is_post_limit_expired(
        user.post_limits_expiration_time
    ):
        cooldown = 24
        if user.id <= 100:
            await update_user(
                session=session, tg_id=callback.from_user.id, daily_post_count=2
            )

        new_expiration_time = datetime.now(timezone.utc) + timedelta(
            hours=cooldown // user.daily_post_count
        )
        await update_user(
            session=session,
            tg_id=callback.from_user.id,
            post_limits_expiration_time=new_expiration_time,
        )

        await state.clear()
        await state.set_state(UserState.name)
        await callback.message.answer(sell_asic_msgs.get("name"))
        await callback.answer()
    else:
        time_left = calculate_time_left(user.post_limits_expiration_time)
        await callback.message.answer(
            text=post_limit_message.format(time_left=time_left),
            reply_markup=inline_keyboard(
                buttons=[
                    inline_button(text="Главное меню", callback_data="next"),
                ]
            ),
        )
        await callback.answer()


@router.message(UserState.name, F.text)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserState.product)
    await message.answer(text=sell_asic_msgs.get("product"))


@router.message(UserState.product, F.text, valid_product_filter)
async def process_product(
    message: types.Message,
    state: FSMContext,
    product: str,
):
    await state.update_data(product=product)
    await state.set_state(UserState.products_count)
    await message.answer(text=sell_asic_msgs.get("products_count"))


@router.message(UserState.product)
async def process_invalid_product(message: types.Message):
    await message.answer(text=sell_asic_error_msgs.get("error_product"))


@router.message(UserState.products_count, F.text, valid_products_count_filter)
async def process_products_count(
    message: types.Message,
    state: FSMContext,
    products_count: str,
):
    await state.update_data(products_count=products_count)
    await state.set_state(UserState.condition)
    await message.answer(
        text=sell_asic_msgs.get("condition"),
        reply_markup=inline_keyboard(
            buttons=[
                inline_button(text="Новое", callback_data="Новое"),
                inline_button(text="Б/У", callback_data="Б/У"),
                inline_button(text="Разное", callback_data="Разное"),
            ]
        ),
    )


@router.message(UserState.products_count)
async def process_invalid_products_count(message: types.Message):
    await message.answer(text=sell_asic_error_msgs.get("error_products_count"))


@router.callback_query(UserState.condition)
async def process_condition(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(condition=callback.data)
    await state.set_state(UserState.price)
    await callback.message.answer(text=f"Выбранное состояние: {callback.data}")
    await callback.message.answer(text=sell_asic_msgs.get("price"))
    await callback.answer()


@router.message(UserState.price, F.text, valid_price_filter)
async def process_price(
    message: types.Message,
    state: FSMContext,
    price: str,
):
    await state.update_data(price=price)
    await state.set_state(UserState.currency)
    await message.answer(
        text=sell_asic_msgs.get("currency"),
        reply_markup=inline_keyboard(
            buttons=[
                inline_button(text="Рубли", callback_data="РУБ"),
                inline_button(text="USDT", callback_data="USDT"),
            ]
        ),
    )


@router.message(UserState.price)
async def process_invalid_price(message: types.Message):
    await message.answer(text=sell_asic_error_msgs.get("error_price"))


@router.callback_query(UserState.currency)
async def process_currency(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(currency=callback.data)
    await state.set_state(UserState.city)
    await callback.message.answer(text=sell_asic_msgs.get("city"))
    await callback.answer()


@router.message(UserState.city, F.text, valid_city_filter)
async def process_city(message: types.Message, state: FSMContext, city: str):
    await state.update_data(city=city)
    await state.set_state(UserState.is_delivery_company)
    await message.answer(
        text=sell_asic_msgs.get("is_delivery_company"),
        reply_markup=inline_keyboard(
            buttons=[
                inline_button(text="Да", callback_data="Да"),
                inline_button(text="Нет", callback_data="Нет"),
            ]
        ),
    )


@router.message(UserState.city)
async def process_invalid_city(message: types.Message):
    await message.answer(text=sell_asic_error_msgs.get("error_city"))


@router.callback_query(UserState.is_delivery_company)
async def process_is_delivery_company(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(is_delivery_company=callback.data)
    await state.set_state(UserState.phone_number)
    await callback.message.answer(text=sell_asic_msgs.get("phone_number"))
    await callback.answer()


@router.message(UserState.phone_number, F.text, valid_phone_number_filter)
async def process_phone_number(
    message: types.Message,
    state: FSMContext,
    phone_number: str,
):
    await state.update_data(phone_number=phone_number)
    await state.set_state(UserState.telegram_username)
    await message.answer(text=sell_asic_msgs.get("telegram_username"))


@router.message(UserState.phone_number)
async def process_invalid_phone_number(message: types.Message):
    await message.answer(text=sell_asic_error_msgs.get("error_phone_number"))


@router.message(UserState.telegram_username, F.text, valid_telegram_username_filter)
async def process_telegram_username(
    message: types.Message,
    state: FSMContext,
    telegram_username: str,
):
    await state.update_data(telegram_username=telegram_username)
    await state.set_state(UserState.comment)

    await message.answer(text=sell_asic_msgs.get("comment"))


@router.message(UserState.telegram_username)
async def process_invalid_telegram_username(message: types.Message):
    await message.answer(text=sell_asic_error_msgs.get("error_telegram_username"))


@router.message(UserState.comment, F.text, valid_comment_filter)
async def process_comment(
    message: types.Message,
    state: FSMContext,
    comment: str,
):
    await state.update_data(comment=comment, telegram_id=message.from_user.id)
    post = await state.get_data()

    await message.answer(
        text="Ваш пост:\n" + format_post(post=post),
        reply_markup=inline_keyboard(
            buttons=[
                inline_button(text="Опубликовать ✅", callback_data="correct"),
                inline_button(text="Изменить 🔄", callback_data="sell_asic"),
            ]
        ),
    )


@router.message(UserState.comment)
async def process_invalid_comment_length(message: types.Message):
    await message.answer(text=sell_asic_error_msgs.get("error_comment"))
