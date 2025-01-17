from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    PreCheckoutQuery,
    Message,
    LabeledPrice,
)
from config.config import bot, settings
from aiogram.enums import ContentType
from keyboards.user_kb import payment_kb, main_menu

router = Router()


@router.callback_query(F.data == "payment")
async def payment_method(call: CallbackQuery):
    await call.message.edit_text(
        "Здесь вы можете выбрать необходимую сумму, чтобы поблагодарить нас за бота",
        reply_markup=payment_kb().as_markup(),
    )


@router.callback_query(lambda c: c.data and c.data.startswith("pay:"))
async def pay_stars(call: CallbackQuery):
    stars = int(call.data.split(":")[1])
    await call.answer(cache_time=1)
    await bot.send_invoice(
        chat_id=call.from_user.id,
        title="✨ Благодарим за вашу поддержку!",
        description="Мы невероятно признательны за вашу помощь и поддержку. Ваш вклад помогает нам становиться лучше! 🌟",
        payload="donate_" + str(stars),
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label="⭐️ Донат", amount=stars)],  # сумма в копейках
        start_parameter="donate",
    )


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    await message.answer(
        text=f"Мы невероятно признательны за вашу помощь и поддержку. Ваш вклад помогает нам становиться лучше! 🌟",
        message_effect_id="5046509860389126442",
        reply_markup=main_menu(),
    )
    await bot.refund_star_payment(
        user_id=message.chat.id,
        telegram_payment_charge_id=message.successful_payment.telegram_payment_charge_id,
    )
    await bot.send_message(
        chat_id=settings.ADMIN_ID,
        text=(
            "🎉 Успешный донат! 🎉\n\n"
            f"👤 Пользователь: @{message.from_user.username}\n"
            f"🆔 ID: {message.from_user.id}\n"
            f"💰 Сумма платежа: {message.successful_payment.total_amount} 🌟"
        ),
    )
