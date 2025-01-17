from faststream import FastStream
from faststream.redis import RedisBroker
from db.dao_class import SubscribeDAO, GetUser
from db.database import connection
from loguru import logger
from config.config import bot
from datetime import datetime
from keyboards.user_kb import phone_kb
import asyncio

broker = RedisBroker("redis://localhost:6379")
app = FastStream(broker)


@broker.subscriber("broadcast_message")
async def broadcast_message(data):
    print(f"Получено сообщение: {data}")
    await bot_message(
        phone=data["phones"],
        message=data["cleaned_message"],
        category=data["closest_category"],
        region=data["region"],
    )
    return True


@connection()
async def bot_message(phone: str, message: str, category: str, region: str, session):
    good_send = 0
    bad_send = 0

    # Получение пользователей
    users = await SubscribeDAO.find_all(
        session=session,
        filters=GetUser(region=region, category=category),
    )

    # Логируем количество найденных пользователей
    if not users:
        logger.info("Список пользователей пуст, отправка не требуется")
        return good_send, bad_send

    # logger.info(f"Найдено пользователей для отправки: {len(users)}")

    # Формирование сообщения
    send_message = (
        "📢 Новый заказ:\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 Категория: {category}\n"
        f"📅 Дата: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"🌍 Регион: {region}\n"
        f"💬 Комментарий: {message}\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "🤝 Наша группа в телеграмм:\n"
        "https://t.me/Spetstekhnika_free"
        "\n"
        "━━━━━━━━━━━━━━━━━━━\n"
    )

    # Цикл отправки сообщений
    try:
        for user in users:
            try:

                # logger.debug(f"Отправка сообщения пользователю {user.telegram_id}")
                await bot.send_message(
                    chat_id=user.telegram_id,
                    text=send_message,
                    reply_markup=phone_kb(phone=phone).as_markup(),
                    disable_web_page_preview=True,
                )
                good_send += 1  # Успешная отправка
            except Exception as e:
                # logger.info(f"Ошибка отправки пользователю {user.telegram_id}: {e}")
                bad_send += 1
            await asyncio.sleep(0.3)

    except Exception as e:
        logger.error(f"Ошибка во время выполнения цикла отправки: {e}")

    finally:
        # Лог отправки в любом случае
        logger.info(f"Успешно отправлено: {good_send}, Не удалось: {bad_send}")

    return good_send, bad_send
