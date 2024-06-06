from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from handlers.users.morning_workout.morning_workout import plan_morning_workout_handler
from handlers.users.reminder import notify_user_schedule, notify_user
from keyboards.inline.choose_frequency_and_time import frequency_calendar_callback
from loader import dp
from utils.db_api import quick_commands as commands


@dp.message_handler(Command("test"))
async def testing_commands(message: types.Message, dialog_manager: DialogManager):
    testing = await commands.get_last_workout(user_id=message.from_user.id)
    print(testing)
    await message.answer(f'{testing}')


# @dp.callback_query_handler(frequency_calendar_callback.filter())
# async def frequency_calendar_callback_as(call: CallbackQuery):
#     print("got")
