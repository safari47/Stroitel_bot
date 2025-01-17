from datetime import datetime
from sqlalchemy import func, TIMESTAMP, text, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)
from functools import wraps
from loguru import logger

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    @classmethod
    @property
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

    def to_dict(self) -> dict:
        # Метод для преобразования объекта в словарь
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def connection(isolation_level=None):
    def decorator(method):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            async with async_session_maker() as session:
                try:
                    # Устанавливаем уровень изоляции, если передан
                    if isolation_level:
                        await session.execute(
                            text(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}")
                        )

                    # Выполняем декорированный метод
                    result = await method(*args, session=session, **kwargs)

                    # Здесь вы можете зафиксировать изменения, если нужно
                    await session.commit()

                    return result
                except Exception as e:
                    await session.rollback()  # Откатываем сессию при ошибке
                    logger.error(e)  # Поднимаем исключение дальше
                finally:
                    await session.close()  # Закрываем сессию

        return wrapper

    return decorator
