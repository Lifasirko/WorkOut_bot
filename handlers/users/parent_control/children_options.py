from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from handlers.users.morning_workout.morning_workout import plan_morning_workout_handler
from keyboards.inline.callback_datas import children_menu_callback, choose_children_callback, \
    set_children_workout_callback, get_children_statistics_callback, get_children_finish_workout_callback
from keyboards.inline.children_menu import children_menu_func, child_menu_func
from loader import dp
from utils.db_api import quick_commands as commands


@dp.callback_query_handler(children_menu_callback.filter())
async def children_menu(call: CallbackQuery):
    await call.message.edit_reply_markup()
    markup = await children_menu_func(user_id=call.from_user.id)
    await call.message.answer(text="Оберіть опцію", reply_markup=markup)


@dp.callback_query_handler(choose_children_callback.filter())
async def child_menu(call: CallbackQuery, callback_data: dict):
    child_id = int(callback_data.get("child_id"))
    child_name = callback_data.get("child_name")
    await call.message.edit_reply_markup()
    markup = await child_menu_func(child_id, child_name)
    await call.message.answer(text=f"Оберіть опцію для {child_name}", reply_markup=markup)


@dp.callback_query_handler(set_children_workout_callback.filter())
async def set_children_workout(call: CallbackQuery, callback_data: dict, dialog_manager: DialogManager):
    child_id = int(callback_data.get("child_id"))
    child_name = callback_data.get("child_name")
    await call.message.edit_reply_markup()
    await plan_morning_workout_handler(call=call, dialog_manager=dialog_manager, updating_user_id=child_id)


@dp.callback_query_handler(get_children_statistics_callback.filter())
async def set_children_workout(call: CallbackQuery, callback_data: dict):
    child_id = int(callback_data.get("child_id"))
    child_name = await commands.get_user_real_name(telegram_id=child_id)
    await call.message.edit_reply_markup()
    markup = await child_menu_func(child_id, child_name)
    await call.message.answer("Ця функція поки не налаштована. Буде згодом.", reply_markup=markup)


@dp.callback_query_handler(get_children_finish_workout_callback.filter())
async def set_children_workout(call: CallbackQuery, callback_data: dict):
    child_id = int(callback_data.get("child_id"))
    child_name = await commands.get_user_real_name(telegram_id=child_id)
    await call.message.edit_reply_markup()
    markup = await child_menu_func(child_id, child_name)
    await call.message.answer("Ця функція поки не налаштована. Буде згодом.", reply_markup=markup)
