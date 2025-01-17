from aiogram import Router, F
from aiogram.types import CallbackQuery
from db.dao_class import UserDAO, SubscribeDAO, TelegramIDModel
from db.database import connection
from keyboards.user_kb import main_menu
from collections import defaultdict

router = Router()


@router.callback_query(F.data == "profile")
@connection()
async def on_phone_button_click(call: CallbackQuery, session):
    await call.answer("ПРОФИЛЬ ...")
    # Получаем данные пользователя из базы
    user = await UserDAO.find_one_or_none(
        session=session, filters=TelegramIDModel(telegram_id=call.from_user.id)
    )

    # Получаем подписки пользователя
    subscriptions = await SubscribeDAO.find_all(
        session=session, filters=TelegramIDModel(telegram_id=call.from_user.id)
    )

    # Формируем структуру подписок (группируем по регионам)
    subscriptions_dict = defaultdict(list)
    for sub in subscriptions:
        subscriptions_dict[sub.region].append(sub.category)

    # Формируем строку с информацией о подписках
    subscriptions_info = ""
    if subscriptions_dict:
        for region, categories in subscriptions_dict.items():
            subscriptions_info += f"▫️ Регион: {region}\n"
            subscriptions_info += "📂 Категории:\n"
            for category in categories:
                subscriptions_info += f"   ├─ {category}\n"
    else:
        subscriptions_info = "Нет активных подписок."

    # Формируем сообщение профиля
    profile_message = (
        f"🗒 Ваш Профиль\n\n"
        f"👤 Имя: {user.first_name or 'Не указано'}\n"
        f"👥 Фамилия: {user.last_name or 'Не указана'}\n"
        f"🔗 Юзернейм: @{user.username or 'Не указана'}\n"
        f"🆔 Telegram ID: {user.telegram_id}\n"
        f"📅 Дата регистрации: {user.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        f"📌 Ваши подписки:\n{subscriptions_info}"
    )

    # Отправляем сообщение с профилем
    await call.message.edit_text(text=profile_message, reply_markup=main_menu())
