from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config.filter import categories_dict, region
from config.config import settings


def main_kb(user_id):
    keyboard = [
        [InlineKeyboardButton(text="🌎 ВЫБРАТЬ РЕГИОН", callback_data="earth")],
        [
            InlineKeyboardButton(
                text="🚜 ВЫБРАТЬ СПЕЦТЕХНИКУ", callback_data="technique"
            )
        ],
        [InlineKeyboardButton(text="💸 ОТБЛАГОДАРИТЬ", callback_data="payment")],
        [InlineKeyboardButton(text="ℹ️ МОЙ ПРОФИЛЬ", callback_data="profile")],
    ]
    # if user_id == settings.ADMIN_ID:
    #     keyboard.append(
    #         [InlineKeyboardButton(text="🔓 АДМИНКА", callback_data="admin_panel")]
    #     )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def auto_kb(data):
    # Получаем данные по ключу 'category'
    active_cat = [record.category for record in data]
    print(active_cat)
    builder = InlineKeyboardBuilder()
    for cat, value in categories_dict.items():
        text = f"✅ {cat}" if cat in active_cat else cat
        builder.button(text=text, callback_data=f"set:auto:{cat}")

    builder.adjust(2)
    builder.attach(InlineKeyboardBuilder.from_markup(main_menu()))

    return builder


def region_kb(reg):
    builder = InlineKeyboardBuilder()
    for r in region:
        text = f"✅ {r}" if r == reg else r
        builder.button(text=text, callback_data=f"set:region:{r}")
    builder.adjust(1)
    builder.attach(InlineKeyboardBuilder.from_markup(main_menu()))
    return builder


# def admin_kb():
#     builder = InlineKeyboardBuilder()
#     builder.button(text="➕ ДОБАВИТЬ ГРУППУ", callback_data="add_chanel")
#     builder.button(text="➖ УДАЛИТЬ ГРУППУ", callback_data="del_chanel")
#     builder.attach(InlineKeyboardBuilder.from_markup(main_menu()))
#     builder.adjust(1)
#     return builder


def phone_kb(phone):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"📲 ПОКАЗАТЬ НОМЕР", callback_data=f"hide:phone:{phone}")
    return builder


def main_menu():
    keyboard = [
        [InlineKeyboardButton(text="🔙 ГЛАВНОЕ МЕНЮ", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def payment_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="50 ⭐️", callback_data="pay:50")
    builder.button(text="100 ⭐️", callback_data="pay:100")
    builder.button(text="250 ⭐️", callback_data="pay:250")
    builder.button(text="500 ⭐️", callback_data="pay:500")
    builder.button(text="1000 ⭐️", callback_data="pay:1000")
    builder.attach(InlineKeyboardBuilder.from_markup(main_menu()))
    builder.adjust(1)
    return builder
