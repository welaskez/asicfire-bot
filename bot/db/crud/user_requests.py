from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.models.user import User


async def create_user(session: AsyncSession, tg_id: int) -> User:
    user = User(tg_id=tg_id)

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def update_user(session: AsyncSession, tg_id: int, **kwargs) -> None:
    user = await get_user_by_tg_id(session=session, tg_id=tg_id)
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value)
        await session.commit()
        await session.refresh(user)


async def get_user_by_tg_id(session: AsyncSession, tg_id: int) -> User | None:
    return await session.scalar(select(User).where(User.tg_id == tg_id))


async def get_user(session: AsyncSession) -> list[User]:
    return await session.scalars(select(User))
