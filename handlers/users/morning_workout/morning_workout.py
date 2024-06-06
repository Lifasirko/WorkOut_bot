import datetime

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from data.dates import days_fullname_dict
from keyboards.inline.back_to_options_button import back_to_options_button
from keyboards.inline.callback_datas import workout_schedule_callback
from keyboards.inline.change_user_data_menu import get_user_timezone_button_func
from keyboards.inline.children_menu import child_menu_func
from keyboards.inline.choose_frequency_and_time import frequency_calendar_callback, \
    FrequencyCalendar, Register
from loader import dp
from utils.db_api import quick_commands as commands


@dp.callback_query_handler(workout_schedule_callback.filter())
async def plan_morning_workout_handler(call: CallbackQuery, dialog_manager: DialogManager,
                                       updating_user_id: int = None):
    if updating_user_id is not None:
        updating_user_id = updating_user_id
    else:
        await call.message.edit_reply_markup()
        updating_user_id = call.from_user.id
    await commands.add_workout_schedule(user_id=updating_user_id)
    await dialog_manager.start(Register.hello, mode=StartMode.RESET_STACK, data={"updating_user_id": updating_user_id})


@dp.callback_query_handler(frequency_calendar_callback.filter())
async def process_dialog_calendar(call: CallbackQuery, callback_data: dict, dialog_manager: DialogManager):
    selected, date = await FrequencyCalendar().frequency_selection(call, callback_data)
    if selected:
        hour = int(callback_data.get('hour'))
        minute = int(callback_data.get('minute'))
        chosen_days = callback_data.get('chosen_days')
        updating_user_id = int(callback_data.get('updating_user_id'))

        chosen_days_list = list(chosen_days.split(', '))
        chosen_days_all = []
        for day in chosen_days_list:
            day = int(day)
            chosen_days_one = days_fullname_dict.get(day)
            chosen_days_all.append(chosen_days_one)
        chosen_days_all_string = ", ".join(
            str(chosen_days_all) for index, chosen_days_all in enumerate(chosen_days_all))
        time = datetime.time(hour=hour, minute=minute)
        tz = await commands.get_timezone(telegram_id=updating_user_id)
        if updating_user_id == call.from_user.id:
            if tz:
                markup = back_to_options_button
                await call.message.answer(
                    f'Ми будемо нагадувати вам про тренування у такі дні:\n'
                    f'{chosen_days_all_string}\n'
                    f'о {time.strftime("%H:%M")}',
                    reply_markup=markup)
            else:
                user_id = updating_user_id
                markup = await get_user_timezone_button_func(user_id)
                await call.message.answer(
                    f'Ми будемо нагадувати вам про тренування у такі дні:\n'
                    f'{chosen_days_all_string}\n'
                    f'о {time.strftime("%H:%M")}\n'
                    f'Проте для коректної роботи нагадувань необхідно вказати часовий пояс.',
                    reply_markup=markup)
        else:
            child_name = await commands.get_user_real_name(telegram_id=updating_user_id)
            if tz:
                markup = await child_menu_func(child_id=updating_user_id, child_name=child_name)
                await call.message.answer(
                    f'Ми будемо нагадувати вашій дитині ({child_name}) про тренування у такі дні:\n'
                    f'{chosen_days_all_string}\n'
                    f'о {time.strftime("%H:%M")}',
                    reply_markup=markup)
            else:
                user_id = updating_user_id
                markup = await get_user_timezone_button_func(user_id)
                await call.message.answer(
                    f'Ми будемо нагадувати вашій дитині ({child_name}) про тренування у такі дні:\n'
                    f'{chosen_days_all_string}\n'
                    f'о {time.strftime("%H:%M")}\n'
                    f'Проте для коректної роботи нагадувань необхідно вказати її часовий пояс.',
                    reply_markup=markup)  # TODO: поставить часовой пояс ребенка через родителя через state data

        await commands.update_scheduled_reminder(telegram_id=updating_user_id)
        if "Понеділок" in chosen_days_all_string:
            # print("Понеділок got!")
            await commands.add_monday_workout(user_id=updating_user_id, time=time)
        if "Вівторок" in chosen_days_all_string:
            # print("Вівторок got!")
            await commands.add_tuesday_workout(user_id=updating_user_id, time=time)
        if "Середа" in chosen_days_all_string:
            # print("Середа got!")
            await commands.add_wednesday_workout(user_id=updating_user_id, time=time)
        if "Четвер" in chosen_days_all_string:
            # print("Четвер got!")
            await commands.add_thursday_workout(user_id=updating_user_id, time=time)
        if "П'ятниця" in chosen_days_all_string:
            # print("П'ятниця got!")
            await commands.add_friday_workout(user_id=updating_user_id, time=time)
        if "Субота" in chosen_days_all_string:
            # print("Субота got!")
            await commands.add_saturday_workout(user_id=updating_user_id, time=time)
        if "Неділя" in chosen_days_all_string:
            # print("Неділя got!")
            await commands.add_sunday_workout(user_id=updating_user_id, time=time)
        await dialog_manager.done()
