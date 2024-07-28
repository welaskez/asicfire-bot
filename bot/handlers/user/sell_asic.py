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

from keyboards.inline import inline_keyboard, inline_button

from utils.messages import end
from utils.helpers import format_post, decode_redis_hash

from states import UserState

from redis.asyncio import Redis

import config

router = Router()


@router.callback_query(F.data == "sell_asic")
async def sell_asic_cmd(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.name)
    await callback.message.answer("Как вас зовут?")
    await callback.answer()


@router.message(UserState.name, F.text)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserState.product)
    await message.answer(
        text="Что вы хотите продать?\n(Производитель, хешрейт)\n\n<i>Например: Whatsminer M50 120 TH</i>"
    )


@router.message(UserState.product, F.text, valid_product_filter)
async def process_product(
    message: types.Message,
    state: FSMContext,
    product: str,
):
    await state.update_data(product=product)
    await state.set_state(UserState.products_count)
    await message.answer(text="Сколько у вас устройств?\n<i>Напишите число</i>")


@router.message(UserState.product)
async def process_invalid_product(message: types.Message):
    await message.answer(
        text="Слишком длинное название.\n<i>Попробуйте так: Atnminer S21 200 TH</i>"
    )


@router.message(UserState.products_count, F.text, valid_products_count_filter)
async def process_products_count(
    message: types.Message,
    state: FSMContext,
    products_count: str,
):
    await state.update_data(products_count=products_count)
    await state.set_state(UserState.condition)
    await message.answer(
        text="В каком они состоянии?",
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
    await message.answer(
        "Вы уверены, что хотите продать больше десяти "
        "тысяч устройств?\n\n<i>Напишите заново количество цифрами</i>"
    )


@router.callback_query(UserState.condition)
async def process_condition(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(condition=callback.data)
    await state.set_state(UserState.price)
    await callback.message.answer(f"Выбранное состояние: {callback.data}")
    await callback.message.answer(
        "Напишите цену, за которую хотите продать.\n\n<i>Просто цифру, а затем валюту</i>"
    )
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
        text="Рубли или usdt?",
        reply_markup=inline_keyboard(
            buttons=[
                inline_button(text="Рубли", callback_data="РУБ"),
                inline_button(text="USDT", callback_data="USDT"),
            ]
        ),
    )


@router.message(UserState.price)
async def process_invalid_price(message: types.Message):
    await message.answer("Цена слишком большая, попробуйте еще раз")


@router.callback_query(UserState.currency)
async def process_currency(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(currency=callback.data)
    await state.set_state(UserState.city)
    await callback.message.answer(text="В каком городе асики?")
    await callback.answer()


@router.message(UserState.city, F.text, valid_city_filter)
async def process_city(message: types.Message, state: FSMContext, city: str):
    await state.update_data(city=city)
    await state.set_state(UserState.is_delivery_company)
    await message.answer(
        text="Отправите транспортной компанией?",
        reply_markup=inline_keyboard(
            buttons=[
                inline_button(text="Да", callback_data="Да"),
                inline_button(text="Нет", callback_data="Нет"),
            ]
        ),
    )


@router.message(UserState.city)
async def process_invalid_city(message: types.Message):
    await message.answer(text="Название города слишком длинное, попробуйте еще раз")


@router.callback_query(UserState.is_delivery_company)
async def process_is_delivery_company(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(is_delivery_company=callback.data)
    await state.set_state(UserState.phone_number)
    await callback.message.answer(
        text="Способ связи с вами:\n<i>Номер телефона в любом формате:</i>"
    )
    await callback.answer()


@router.message(UserState.phone_number, F.text, valid_phone_number_filter)
async def process_phone_number(
    message: types.Message,
    state: FSMContext,
    phone_number: str,
):
    await state.update_data(phone_number=phone_number)
    await state.set_state(UserState.telegram_username)
    await message.answer(text="<i>Ваш telegram юзернейм @</i>")


@router.message(UserState.phone_number)
async def process_invalid_phone_number(message: types.Message):
    await message.answer("Неверный формат номера телефона, попробуйте еще раз")


@router.message(UserState.telegram_username, F.text, valid_telegram_username_filter)
async def process_telegram_username(
    message: types.Message,
    state: FSMContext,
    telegram_username: str,
):
    await state.update_data(telegram_username=telegram_username)
    await state.set_state(UserState.comment)

    await message.answer(
        text="Хотите дополнить объявление комментарием?\n\n<i>Не более 140 симоволов."
        "\nПожалуйста, не используйте ссылки (сразу удалим)</I>"
    )


@router.message(UserState.telegram_username)
async def process_invalid_telegram_username(message: types.Message):
    await message.answer("Слишком длинный юзернейм, попробуйте еще раз")


@router.message(UserState.comment, F.text, valid_comment_filter)
async def process_comment(
    message: types.Message,
    state: FSMContext,
    comment: str,
):
    await state.update_data(comment=comment)
    await state.update_data(telegram_id=message.from_user.id)
    post = await state.get_data()
    await message.answer(
        text="Ваш пост:\n" + format_post(post=post),
        reply_markup=inline_keyboard(
            buttons=[
                inline_button(text="Опубликовать ✅", callback_data="correct"),
                inline_button(text="Изменить 🔄", callback_data="incorrect"),
            ]
        ),
    )


@router.message(UserState.comment)
async def process_invalid_comment_length(message: types.Message):
    await message.answer("Комментарий слишком длинный!")


@router.callback_query(F.data == "correct")
async def send_post_to_admin(
    callback: types.CallbackQuery,
    state: FSMContext,
    r: Redis,
):
    post = await state.get_data()

    await r.hmset(name=f"user:{callback.from_user.id}", mapping=post)

    await callback.message.answer(
        text=end,
        reply_markup=inline_keyboard(
            buttons=[inline_button(text="Продолжить", callback_data="next")]
        ),
    )
    await callback.answer()

    await callback.message.bot.send_message(
        chat_id=config.ADMINS[0],
        text="Новый пост!\n" + format_post(post=post),
        reply_markup=inline_keyboard(
            buttons=[
                inline_button(
                    text="Опубликовать",
                    callback_data=f"publish_post:{callback.from_user.id}",
                ),
                inline_button(
                    text="Не опубликовывать",
                    callback_data=f"dont_publish_post:{callback.from_user.id}",
                ),
            ]
        ),
    )
    await state.set_state(UserState.publish_post)
    await callback.answer()


@router.callback_query(F.data.startswith("publish_post:"))
async def publish_post(callback: types.CallbackQuery, r: Redis):
    user_id = int(callback.data.split(":")[1])
    post = decode_redis_hash(await r.hgetall(f"user:{user_id}"))

    await callback.message.answer("⬆️ ОПУБЛИКОВАН")
    await callback.message.bot.send_message(
        chat_id=config.CHANEL_USERNAME,
        text=format_post(post),
    )
    await callback.message.bot.send_message(
        chat_id=int(post.get("telegram_id")),
        text="✅ Ваше объявление опубликовано",
    )
    await callback.answer()
    await r.delete(f"user:{user_id}")


@router.callback_query(F.data == "next")
async def next_cmd(callback: types.CallbackQuery):
    await callback.message.answer_photo(
        photo=types.FSInputFile(f"{config.BASE_DIR}/imgs/img.jpg"),
        caption="📲 Если вам требуется срочно продать устройство - заполните объявление, и мы "
        "разместим его в удобном формате\n\nУзнать информацию о продавце - @asicfirechat",
        reply_markup=inline_keyboard(
            buttons=[
                inline_button(text="Продать устройство", callback_data="sell_asic"),
                inline_button(
                    text="Экосистема poolproof", callback_data="ecosystem_poolproof"
                ),
            ]
        ),
    )


@router.callback_query(F.data.startswith("dont_publish_post:"))
async def dont_publish_post(callback: types.CallbackQuery, r: Redis):
    user_id = int(callback.data.split(":")[1])
    post = await r.hgetall(f"user:{user_id}")

    await callback.message.answer("⬆️ НЕ ОПУБЛИКОВАН")
    await callback.message.bot.send_message(
        chat_id=int(post.get("telegram_id")),
        text="🚫 Ваш пост не прошел проверку\n\nСвяжитесь с @asicfire_admin",
    )
    await callback.answer()
    await r.delete(f"user:{user_id}")


async def incorrect_data(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()

    await state.set_state(UserState.name)
    await callback.message.answer("Как вас зовут?")
    await callback.answer()
