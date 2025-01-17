import os
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from pyrogram import Client
from logging.handlers import RotatingFileHandler
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from faststream.redis import RedisBroker


# Класс настроек
class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_ID: int
    API_ID: int
    API_HASH: str
    PHONE: str
    LOGIN: str
    REDIS_PORT: int  # Порт для подключения к Redis
    REDIS_HOST: str  # Хост Redis-сервера
    REDIS_DB: int
    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"
    # Загрузка переменных из .env
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


# Получаем параметры настроек
settings = Settings()

# Инициализируем aiogram бота и диспетчер
bot = Bot(
    token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
storage = RedisStorage.from_url(
    f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
)
dp = Dispatcher(storage=storage)
# Инициализируем pyrogram бота
client = Client(
    name="myaccount",
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    phone_number=settings.PHONE,
)

redis_url = f"rediss://:{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

broker = RedisBroker(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")

# Настройка логирования
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")

# Ротация логов: создается максимум 5 файлов, размер каждого до 10 MB
rotating_handler = RotatingFileHandler(
    log_file_path, maxBytes=10_000_000, backupCount=5
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Логи будут выводиться в консоль
        logging.FileHandler(
            log_file_path, encoding="utf-8"
        ),  # Логи будут писаться в файл
    ],
)
logger = logging.getLogger(__name__)

# logger.add(
#     log_file_path,
#     format=settings.FORMAT_LOG,
#     level="INFO",
#     rotation=settings.LOG_ROTATION,
# )
# logger=logging.getLogger()
