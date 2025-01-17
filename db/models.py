from datetime import datetime
from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class User(Base):
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    date_subscribed: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    def __repr__(self):
        return (
            f"<User(telegram_id={self.telegram_id}, "
            f"first_name={self.first_name}, "
            f"last_name={self.last_name}, "
            f"username={self.username}, "
            f"date_subscribed={self.date_subscribed})>"
        )


class Subscribe(Base):
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    region: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f"<Subscribe(telegram_id={self.telegram_id}, region={self.region}, category={self.category})>"
