start = """
Привет.
Это бот @asicfire

📲 Если вам требуется срочно продать устройство - заполните объявление, и мы разместим его в удобном формате

💬 Узнать информацию о продавце - @asicfirechat
"""

error_not_text = """
Упс, что то пошло не так :(
Напишите сообщение текстом и попробуйте снова
"""

end = "👌 Ваше объявление проходит проверку администратором."

post_template = """
<b>Продавец</b>: {}
<b>Товар</b>: {}
<b>Количество</b>: {}
<b>Состояние</b>: {}
<b>Цена</b>: {} {}
<b>Город</b>: {}
<b>Доставка тп</b>: {}
<b>Комментарий</b>: {}

<b>Контактные данные</b>:
{}
{}

💬 <b>Обсудить</b> @asicfirechat
📲 <b>Продать</b> @asicfirebot
"""

ecosystem_poolproof_text = """
Экосистема poolproof.tech предлагает решения для майнеров.

POOLPROOF | BOT - бот экосистемы.
История доходности майнинг-пулов, AML-проверки добываемой криптовалюты, техподдержка майнеров. 

THE MINERS CLUB - первая NFT коллекция от майнеров для майнеров на TON Blockchain

Реальная доходность пулов - ежедневная доходность популярных майнинг-пулов
Журнал майнера - новости индустрии майнинга
AsicFire - доска объявления по продаже оборудования
Service - гарантийный ремонт Whatsminer, Antminer, Jasminer. Техподдержка.
"""

faq_text = """
🔽 Пожалуйста, прочитайте это перед размещением объявления 

▫️ Анкета требуется, чтобы объявление было сформировано в читабельный для всех формат.

▫️ Мы просим вас оставить номер, чтобы покупателю было проще связаться.

▫️ Если не хотите оставлять номер, то напишите 70000000000 (десять нулей), но такие объявления реже проходят верификацию от админа.

▫️ В комментарии напишите любую дополнительную информацию. Если вы опубликуете ссылку - объявление не пройдет верификацию. Если у вас есть вопросы по рекламной интеграции компании - напиши администраторам.
"""

# sell_asic handlers msgs

name_msg = "Как вас зовут?"
product_msg = "Что вы хотите продать?\n(Производитель, хешрейт)\n\n<i>Например: Whatsminer M50 120 TH</i>"
products_count_msg = "Сколько у вас устройств?\n<i>Напишите число</i>"
condition_msg = "В каком они состоянии?"
price_msg = (
    "Напишите цену, за которую хотите продать.\n\n<i>Просто цифру, а затем валюту</i>"
)
currency_msg = "Рубли или usdt?"
city_msg = "В каком городе асики?"
is_delivery_company_msg = "Отправите транспортной компанией?"
phone_number_msg = "Способ связи с вами:\n<i>Номер телефона в любом формате:</i>"
telegram_username_msg = "<i>Ваш telegram юзернейм @</i>"
comment_msg = (
    "Хотите дополнить объявление комментарием?\n\n<i>Не более 140 симоволов."
    "\nПожалуйста, не используйте ссылки (сразу удалим)</I>"
)

sell_asic_msgs = {
    "name": name_msg,
    "product": product_msg,
    "products_count": products_count_msg,
    "condition": condition_msg,
    "price": price_msg,
    "currency": currency_msg,
    "city": city_msg,
    "is_delivery_company": is_delivery_company_msg,
    "phone_number": phone_number_msg,
    "telegram_username": telegram_username_msg,
    "comment": comment_msg,
}

# sell asic handlers error msgs
error_product_msg = (
    "Слишком длинное название.\n<i>Попробуйте так: Atnminer S21 200 TH</i>"
)
error_products_count_msg = (
    "Вы уверены, что хотите продать больше десяти "
    "тысяч устройств?\n\n<i>Напишите заново количество цифрами</i>"
)
error_price_msg = "Цена слишком большая, попробуйте еще раз"
error_city_msg = "Название города слишком длинное, попробуйте еще раз"
error_phone_number_msg = "Неверный формат номера телефона, попробуйте еще раз"
error_telegram_username_msg = "Слишком длинный юзернейм, попробуйте еще раз"
error_comment_msg = "Комментарий слишком длинный!"

sell_asic_error_msgs = {
    "error_product": error_product_msg,
    "error_products_count": error_products_count_msg,
    "error_price": error_price_msg,
    "error_city": error_city_msg,
    "error_phone_number": error_phone_number_msg,
    "error_telegram_username": error_telegram_username_msg,
    "error_comment": error_comment_msg,
}
