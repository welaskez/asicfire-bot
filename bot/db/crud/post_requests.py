from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Post


async def create_post(
    session: AsyncSession,
    user_id: int,
    name: str,
    product: str,
    products_count: int,
    condition: str,
    price: int,
    currency: str,
    city: str,
    is_delivery_company: str,
    comment: str,
    phone_number: str,
    telegram_username: str,
    message_id: int,
) -> Post:
    post = Post(
        user_id=user_id,
        name=name,
        product=product,
        products_count=products_count,
        condition=condition,
        price=price,
        currency=currency,
        city=city,
        is_delivery_company=is_delivery_company,
        comment=comment,
        phone_number=phone_number,
        telegram_username=telegram_username,
        message_id=message_id,
    )

    session.add(post)
    await session.commit()
    await session.refresh(post)

    return Post
