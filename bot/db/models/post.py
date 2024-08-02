from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy import text

from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Post(Base):
    name: Mapped[str] = mapped_column(String(35))
    product: Mapped[str] = mapped_column(String(35))
    products_count: Mapped[int]
    condition: Mapped[str]
    price: Mapped[int]
    currency: Mapped[str]
    city: Mapped[str] = mapped_column(String(25))
    is_delivery_company: Mapped[str]
    comment: Mapped[str] = mapped_column(String(140))
    phone_number: Mapped[str] = mapped_column(String(16))
    telegram_username: Mapped[str] = mapped_column(String(32))
    message_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="posts")
