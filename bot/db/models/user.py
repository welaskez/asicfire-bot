from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime
from sqlalchemy import BigInteger

from typing import TYPE_CHECKING

from datetime import datetime

from .base import Base

if TYPE_CHECKING:
    from .post import Post


class User(Base):
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    wallet_address: Mapped[str] = mapped_column(unique=True)
    daily_post_count: Mapped[int] = mapped_column(default=1)
    is_subscribed: Mapped[bool] = mapped_column(default=False)
    post_limits_expiration_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    subscription_expiration_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")
