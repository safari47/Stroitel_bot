from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from db.dao_class import UserModel
from datetime import datetime, timedelta
from db.dao_class import UserDAO, TelegramIDModel
from db.database import connection
from keyboards.user_kb import main_kb
from handlers.aiogram.region import Region
from aiogram.fsm.context import FSMContext
from config.static_msg import WELCOME_MESSAGE

router = Router()


@router.message(CommandStart())
@connection()
async def start(message: Message, command: CommandObject, session, state: FSMContext):
    person = await UserDAO.find_one_or_none(
        session=session, filters=TelegramIDModel(telegram_id=message.from_user.id)
    )
    if not person:
        values = UserModel(
            telegram_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
            date_subscribed=datetime.today() + timedelta(days=3),
        )
        await UserDAO.add(session=session, values=values)
    await state.set_state(Region.region)
    await message.answer(
        WELCOME_MESSAGE,
        reply_markup=main_kb(message.from_user.id),
        parse_mode="MarkdownV2",
    )


@router.callback_query(F.data == "main_menu")
async def set_technique(call: CallbackQuery):
    await call.answer("ГЛАВНОЕ МЕНЮ ...")
    await call.message.edit_text(
        text=WELCOME_MESSAGE,
        reply_markup=main_kb(call.from_user.id),
        parse_mode="MarkdownV2",
    )
