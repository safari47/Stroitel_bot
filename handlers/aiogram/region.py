from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.user_kb import region_kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config.static_msg import (
    REGION_SELECTION_PROGRESS,
    SELECT_REGION_OPTION,
    REGION_SELECTED,
    ALREADY_SELECTED_REGION,
)

router = Router()

# Состояние для выбора региона
class Region(StatesGroup):
    region = State()

@router.callback_query(F.data == "earth")
async def see_region(call: CallbackQuery, state: FSMContext):
    await call.answer(REGION_SELECTION_PROGRESS)
    data = await state.get_data()
    reg = data.get("region", None)
    await call.message.edit_text(
        SELECT_REGION_OPTION,
        reply_markup=region_kb(reg).as_markup(),
        parse_mode="Markdown",
    )

@router.callback_query(F.data.contains("set:region:"))
async def set_region(call: CallbackQuery, state: FSMContext):
    region = call.data.split(":")[2]
    await call.answer(REGION_SELECTION_PROGRESS)
    await state.update_data(region=region)
    await state.set_state(Region.region)
    try:
        await call.message.edit_text(
            REGION_SELECTED.format(region),
            reply_markup=region_kb(region).as_markup(),
            parse_mode="Markdown",
        )
    except Exception:
        await call.answer(ALREADY_SELECTED_REGION.format(region), show_alert=True, parse_mode="Markdown")
