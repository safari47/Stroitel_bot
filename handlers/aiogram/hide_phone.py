from aiogram import Router, F
from aiogram.types import CallbackQuery


router = Router()


@router.callback_query(F.data.contains("hide:phone:"))
async def on_phone_button_click(call: CallbackQuery):
    phone = call.data.split(":")[2]  # Получаем номер телефона из callback_data

    # Добавляем номер телефона в конец текста сообщения
    new_text = call.message.text + f"\n📞 Контактный номер телефона: {str(phone)}"

    # Редактируем текст исходного сообщения
    await call.message.edit_text(
        text=new_text,
        disable_web_page_preview=True,
        # parse_mode='Markdown'
    )

    # Уведомляем пользователя, что текст изменен
    await call.answer("Номер добавлен в сообщение!")
