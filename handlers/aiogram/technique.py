from aiogram import Router, F
from aiogram.types import CallbackQuery
from db.dao_class import SubscribeDAO, SubscribedModel, CategoryModel
from db.database import connection
from keyboards.user_kb import auto_kb
from aiogram.fsm.context import FSMContext
from config.static_msg import (
    NO_REGION_SELECTED,
    TECHNIQUE_SELECTION_PROGRESS,
    SELECT_TECHNIQUE_OPTION,
)

router = Router()


@router.callback_query(F.data == "technique")
@connection()
async def see_technique(call: CallbackQuery, session, state: FSMContext):
    data = await state.get_data()
    reg = data.get("region", False)
    if not reg:
        await call.answer(NO_REGION_SELECTED, show_alert=True, parse_mode="Markdown")
        return
    await call.answer(TECHNIQUE_SELECTION_PROGRESS, parse_mode="Markdown")
    data = await SubscribeDAO.find_all(
        session=session,
        filters=SubscribedModel(telegram_id=call.from_user.id, region=reg),
    )
    await call.message.edit_text(
        SELECT_TECHNIQUE_OPTION.format(region=reg),
        reply_markup=auto_kb(data).as_markup(),
        parse_mode="Markdown",
    )


@router.callback_query(F.data.contains("set:auto:"))
@connection()
async def set_technique(call: CallbackQuery, session, state: FSMContext):
    await call.answer(TECHNIQUE_SELECTION_PROGRESS, parse_mode="Markdown")
    category = call.data.split(":")[2]
    data = await state.get_data()
    reg = data.get("region")
    values = CategoryModel(
        telegram_id=call.from_user.id,
        region=reg,
        category=category,
    )
    # Проверка: новая подписка или удаление
    check_category = await SubscribeDAO.find_one_or_none(
        session=session, filters=values
    )
    if not check_category:
        await SubscribeDAO.add(session=session, values=values)
    else:
        await SubscribeDAO.delete(session=session, filters=values)
    # Обновление списка
    data = await SubscribeDAO.find_all(
        session=session,
        filters=SubscribedModel(telegram_id=call.from_user.id, region=reg),
    )
    await call.message.edit_text(
        SELECT_TECHNIQUE_OPTION.format(region=reg),
        reply_markup=auto_kb(data).as_markup(),
        parse_mode="Markdown",
    )
