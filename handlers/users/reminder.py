import logging
from datetime import datetime, timedelta
from typing import Union

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from pytz import timezone, UnknownTimeZoneError

from data.dates import days_eng_ukr_dict
from keyboards.inline.back_to_options_button import back_to_options_button
from keyboards.inline.callback_datas import plan_next_workout_callback
from keyboards.inline.change_user_data_menu import get_user_timezone_button_func
from keyboards.inline.choose_date_and_time_menu import ChooseDateAndTime, \
    choose_level_for_choose_date_and_time_calendar, choose_level_for_choose_date_and_time_calendar_callback
from keyboards.inline.workout_menu import finish_workout_kb
from loader import dp
from utils.db_api import quick_commands as commands


# from aiogram_calendar import dialog_cal_callback, DialogCalendar

# Та самая функция, которая отдает категории. Она может принимать как CallbackQuery, так и Message.
# Помимо этого, мы в нее можем отправить и другие параметры - category, subcategory, item_id,
# Поэтому ловим все остальное в **kwargs


@dp.callback_query_handler(plan_next_workout_callback.filter())
async def plan_next_workout_handler(message: Union[Message, CallbackQuery]):
    markup = await choose_level_for_choose_date_and_time_calendar()
    if isinstance(message, Message):
        await message.answer(text=f"Вітаю \n"
                                  f"Оберіть час, коли вам нагадати про тренування:\n",
                             reply_markup=markup)
    elif isinstance(message, CallbackQuery):
        await message.message.edit_reply_markup()
        await message.message.answer(text=f"Вітаю \n"
                                          f"Оберіть час, коли вам нагадати про тренування:\n",
                                     reply_markup=markup)


@dp.message_handler(Command("plan_next_workout"))
async def command_plan_next_workout(message: Message):
    await plan_next_workout_handler(message=message)


# dialog calendar usage
@dp.callback_query_handler(choose_level_for_choose_date_and_time_calendar_callback.filter())
async def process_dialog_calendar(call: CallbackQuery, callback_data: dict):
    selected, date = await ChooseDateAndTime().process_selection(call, callback_data)
    if selected:
        day = date.strftime("%A")
        day_to_user = days_eng_ukr_dict.get(day)
        # print(day_to_user)
        await commands.add_next_workout_reminder(telegram_id=call.from_user.id, next_workout_reminder=date)
        tz = await commands.get_timezone(telegram_id=call.from_user.id)
        if tz:
            markup = back_to_options_button
            await call.message.answer(
                f'Ми нагадаємо вам про тренування у {day_to_user}, {date.strftime("%d.%m.%Y о %H:%M")}',
                reply_markup=markup)
        else:
            markup = await get_user_timezone_button_func(user_id=call.from_user.id)
            await call.message.answer(
                f'Ми нагадаємо вам про тренування у {day_to_user}, {date.strftime("%d.%m.%Y о %H:%M")}\n'
                f'Проте для коректної роботи нагадувань необхідно вказати часовий пояс.',
                reply_markup=markup)


async def notify_user():
    u2 = await commands.get_next_workout_reminders()
    for telegram_id, next_workout_reminder, timezone_info in u2:
        if next_workout_reminder is not None:
            year = next_workout_reminder.year
            month = next_workout_reminder.month
            day = next_workout_reminder.day
            hour = next_workout_reminder.hour
            minute = next_workout_reminder.minute
            try:
                tz_user = timezone(timezone_info)
                datetime_now_tz = datetime.now(tz=tz_user).tzinfo
                next_workout_reminder_tz = datetime(year, month, day, hour, minute, tzinfo=datetime_now_tz)
                if datetime.now(tz=tz_user) > next_workout_reminder_tz:
                    next_workout_date = list(str(next_workout_reminder))
                    # print(next_workout_date)
                    next_wo_d = ''.join(next_workout_date[:16])
                    # print("telegram_id:", telegram_id, "; next_workout_reminder:", next_workout_reminder)
                    await dp.bot.send_message(chat_id=telegram_id,
                                              text=f"У вас заплановано тренування на {next_wo_d}")
                    await commands.add_next_workout_reminder(telegram_id=telegram_id, next_workout_reminder=None)
            except UnknownTimeZoneError:
                logging.warning(telegram_id)
                markup = await finish_workout_kb(user_id=telegram_id)
                await dp.bot.send_message(chat_id=telegram_id,
                                          text="У вас заплановане тренування, проте ви не вказали свій часовий пояс.",
                                          reply_markup=markup)


async def notify_user_schedule():
    sr = await commands.get_scheduled_reminders()
    # print("sr = ", sr)
    for telegram_id, scheduled_reminder, timezone_info in sr:
        # print("telegram_id = ", telegram_id)
        if scheduled_reminder is True:
            try:
                tz_user = timezone(timezone_info)
                datetime_now_tz = datetime.now(tz=tz_user).tzinfo

                us = await commands.get_scheduled_day_reminders(telegram_id)
                # print("us", us)
                for user_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday in us:
                    year = datetime.now().year
                    month = datetime.now().month
                    day = datetime.now().day
                    # tz = timezone('UTC')
                    # print("user_id", user_id)
                    # print("thursday", thursday)

                    date = datetime(year, month, day, tzinfo=tz_user)
                    day_name = date.strftime("%A")
                    # print("day_name", day_name)
                    datetime_now = datetime.now(tz=tz_user).time()
                    datetime_now_add_minute = (datetime.now(tz=tz_user) + timedelta(minutes=1)).time()

                    if day_name == 'Monday':
                        monday.replace(tzinfo=datetime_now_tz)
                        if (datetime_now > monday) and (datetime_now_add_minute < monday):
                            await dp.bot.send_message(chat_id=telegram_id,
                                                      text=f"У вас заплановано сьогодні тренування.")
                    if day_name == 'Tuesday':
                        tuesday.replace(tzinfo=datetime_now_tz)
                        if (datetime_now > tuesday) and (datetime_now_add_minute < tuesday):
                            await dp.bot.send_message(chat_id=telegram_id,
                                                      text=f"У вас заплановано сьогодні тренування.")
                    if day_name == 'Wednesday':
                        wednesday.replace(tzinfo=datetime_now_tz)
                        if (datetime_now > wednesday) and (datetime_now_add_minute < wednesday):
                            await dp.bot.send_message(chat_id=telegram_id,
                                                      text=f"У вас заплановано сьогодні тренування.")
                    if day_name == 'Thursday':
                        # print("+")
                        thursday.replace(tzinfo=datetime_now_tz)
                        # print(datetime.now(tz=tz_user).time())
                        # print(thursday)
                        if (datetime_now > thursday) and (datetime_now_add_minute < thursday):
                            await dp.bot.send_message(chat_id=telegram_id,
                                                      text=f"У вас заплановано сьогодні тренування.")
                    if day_name == 'Friday':
                        friday.replace(tzinfo=datetime_now_tz)
                        if (datetime_now > friday) and (datetime_now_add_minute < friday):
                            await dp.bot.send_message(chat_id=telegram_id,
                                                      text=f"У вас заплановано сьогодні тренування.")
                    if day_name == 'Saturday':
                        saturday.replace(tzinfo=datetime_now_tz)
                        if (datetime_now > saturday) and (datetime_now_add_minute < saturday):
                            await dp.bot.send_message(chat_id=telegram_id,
                                                      text=f"У вас заплановано сьогодні тренування.")
                    if day_name == 'Sunday':
                        sunday.replace(tzinfo=datetime_now_tz)
                        if (datetime_now > sunday) and (datetime_now_add_minute < sunday):
                            await dp.bot.send_message(chat_id=telegram_id,
                                                      text=f"У вас заплановано сьогодні тренування.")
            except UnknownTimeZoneError:
                logging.warning(telegram_id)
                markup = await finish_workout_kb(user_id=telegram_id)
                await dp.bot.send_message(chat_id=telegram_id,
                                          text="У вас заплановане тренування, проте ви не вказали свій часовий пояс.",
                                          reply_markup=markup)
