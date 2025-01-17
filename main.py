from config.config import client, dp, bot, broker
from loguru import logger
import asyncio
from aiogram.types import BotCommand, BotCommandScopeDefault
from handlers.aiogram.start import router as start_router
from handlers.aiogram.region import router as reg_router
from handlers.aiogram.technique import router as tech_router
from handlers.aiogram.hide_phone import router as hide_phone
from handlers.aiogram.profile import router as profile_router
from handlers.aiogram.payment import router as payment_router
from db.database import create_tables
from handlers.pyrogram.pyro import keyword_handler
from pyrogram.handlers import MessageHandler


# Функция, которая настроит командное меню (дефолтное для всех пользователей)
async def set_commands():
    commands = [BotCommand(command="start", description="Запуск бота")]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


# Функция, которая выполнится, когда бот запустится
async def start_bot():
    await set_commands()
    await create_tables()

async def setup_broker():
    try:
        # Подключаем брокер (обязательно вызовите connect)
        await broker.connect()
        logger.info("Брокер успешно подключен")
    except Exception as e:
        logger.error(f"Ошибка подключения брокера: {e}")
        raise

async def main():
    # Инициализация брокера
    await setup_broker()
    # Регистрируем хендлеры
    dp.startup.register(start_bot)
    dp.include_router(start_router)
    dp.include_router(reg_router)
    dp.include_router(tech_router)
    dp.include_router(hide_phone)
    dp.include_router(profile_router)
    dp.include_router(payment_router)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await client.start()
        client.add_handler(MessageHandler(keyword_handler))
        await asyncio.gather(dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()), return_exceptions=True)
        
    finally:
        await bot.session.close()
        await client.stop()


if __name__ == "__main__":
    try:
        asyncio.ensure_future(main())
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        logger.info("Program stopped by user")
        loop = asyncio.get_event_loop()
