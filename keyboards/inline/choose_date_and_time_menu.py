import calendar
from datetime import datetime

from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# setting callback_data prefix and parts
from data.dates import hours, months, minutes
from keyboards.inline.back_to_options_button import back_to_options_button_func

choose_level_for_choose_date_and_time_calendar_callback = CallbackData('choose_date_and_time', 'act', 'year', 'month',
                                                                       'day', 'hour', 'minute')
ignore_callback = choose_level_for_choose_date_and_time_calendar_callback.new("IGNORE", -1, -1, -1, -1,
                                                                              -1)  # for buttons with no answer


async def choose_level_for_choose_date_and_time_calendar():
    year = datetime.now().year
    month = datetime.now().month
    last_day_in_month = calendar.monthrange(year, month)[1]
    if (datetime.now().day + 7) > last_day_in_month:
        if month == 12:
            return await ChooseDateAndTime().start_calendar()
        else:
            return await ChooseDateAndTime().get_month_kb(year=year)
    else:
        return await ChooseDateAndTime()._get_days_kb(year, month)


class ChooseDateAndTime:

    def __init__(self, year: int = datetime.now().year, month: int = datetime.now().month):
        self.year = year
        self.month = month

    async def start_calendar(
            self,
            year: int = datetime.now().year
    ) -> InlineKeyboardMarkup:
        inline_kb = InlineKeyboardMarkup(row_width=5)
        # first row - years
        inline_kb.row()
        for value in range(year, year + 2):
            inline_kb.insert(InlineKeyboardButton(
                value,
                callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("SET-YEAR", value, -1, -1, -1,
                                                                                          -1)
            ))
        inline_button_options = await back_to_options_button_func()
        inline_kb.row()
        inline_kb.insert(inline_button_options)
        return inline_kb

    async def get_month_kb(
            self,
            year: int
    ):
        month_now: int = datetime.now().month
        inline_kb = InlineKeyboardMarkup(row_width=6)
        # first row with year button
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))  # Пустая кнопка
        inline_kb.insert(InlineKeyboardButton(
            year,
            callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("START", year, -1, -1, -1, -1)
        ))  # Кнопка с выбранным годом и колбэком назад
        inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))  # Пустая кнопка
        # two rows with 6 months buttons
        inline_kb.row()
        for month in months[0:6]:  # Создание строки с месяцами от 1 до 6
            if int(year) == int(datetime.now().year) and months.index(month) < int(month_now - 1):
                inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
                continue
            inline_kb.insert(InlineKeyboardButton(
                month,
                callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("SET-MONTH", year,
                                                                                          months.index(month) + 1, -1,
                                                                                          -1, -1)
            ))
        inline_kb.row()
        for month in months[6:12]:
            if int(year) == int(datetime.now().year) and months.index(month) < int(month_now):
                inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
                continue
            inline_kb.insert(InlineKeyboardButton(
                month,
                callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("SET-MONTH", year,
                                                                                          months.index(month) + 1, -1,
                                                                                          -1, -1)
            ))
        inline_button_options = await back_to_options_button_func()
        inline_kb.row()
        inline_kb.insert(inline_button_options)

        return inline_kb

    async def _get_days_kb(self, year: int, month: int):
        inline_kb = InlineKeyboardMarkup(row_width=7)
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            year,
            callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("START", year, -1, -1, -1, -1)
        ))  # Кнопка с выбранным годом и колбэком назад
        inline_kb.insert(InlineKeyboardButton(
            months[month - 1],
            callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("SET-YEAR", year, -1, -1, -1, -1)
        ))  # Кнопка с выбранным месяцем и колбэком назад
        inline_kb.row()
        for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]:
            inline_kb.insert(InlineKeyboardButton(day, callback_data=ignore_callback))

        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            inline_kb.row()
            for day in week:
                if day == 0 or (int(year) == int(datetime.now().year) and month == int(
                        datetime.now().month) and day < datetime.now().day):  # and day <= datetime.now().day
                    inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
                    continue
                inline_kb.insert(InlineKeyboardButton(
                    str(day),
                    callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("SET-DAY", year, month,
                                                                                              day, -1, -1)
                ))
        inline_button_options = await back_to_options_button_func()
        inline_kb.row()
        inline_kb.insert(inline_button_options)

        return inline_kb

    async def _get_hours_kb(self, year: int, month: int, day: int):
        inline_kb = InlineKeyboardMarkup(row_width=6)
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            year,
            callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("START", year, -1, -1, -1, -1)
        ))
        inline_kb.insert(InlineKeyboardButton(
            months[month - 1],
            callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("SET-YEAR", year, -1, -1, -1, -1)
        ))  # Кнопка с выбранным месяцем и колбэком назад
        inline_kb.insert(InlineKeyboardButton(
            day,
            callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("SET-DAY", year, month, -1, -1,
                                                                                      -1)
        ))
        inline_kb.row()
        for hour in hours:
            inline_kb.insert(InlineKeyboardButton(
                hour,
                callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("SET-HOUR", year, month, day,
                                                                                          hour, -1)
            ))
        inline_button_options = await back_to_options_button_func()
        inline_kb.row()
        inline_kb.insert(inline_button_options)

        return inline_kb

    async def _get_minutes_kb(self, year: int, month: int, day: int, hour: int):
        inline_kb = InlineKeyboardMarkup(row_width=6)
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            year,
            callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("START", year, -1, -1, -1, -1)
        ))
        inline_kb.insert(InlineKeyboardButton(
            months[month - 1],
            callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("SET-YEAR", year, -1, -1, -1, -1)
        ))  # Кнопка с выбранным месяцем и колбэком назад
        inline_kb.insert(InlineKeyboardButton(
            day,
            callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("SET-DAY", year, month, -1, -1,
                                                                                      -1)
        ))
        inline_kb.insert(InlineKeyboardButton(
            text=f"{hour}:",
            callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("SET-HOUR", year, month, day, -1,
                                                                                      -1)
        ))
        inline_kb.row()
        for minute in minutes:
            inline_kb.insert(InlineKeyboardButton(
                minute,
                callback_data=choose_level_for_choose_date_and_time_calendar_callback.new("SET-MINUTE", year, month,
                                                                                          day, hour, minute)
            ))
        inline_button_options = await back_to_options_button_func()
        inline_kb.row()
        inline_kb.insert(inline_button_options)

        return inline_kb

    async def process_selection(self, call: CallbackQuery, data: CallbackData) -> tuple:
        return_data = (False, None)
        if data['act'] == "IGNORE":
            await call.answer(cache_time=5)
        if data['act'] == "SET-YEAR":
            await call.message.edit_reply_markup(await self.get_month_kb(int(data['year'])))
        if data['act'] == "PREV-YEARS":
            new_year = int(data['year']) - 5
            await call.message.edit_reply_markup(await self.start_calendar(new_year))
        if data['act'] == "NEXT-YEARS":
            new_year = int(data['year']) + 5
            await call.message.edit_reply_markup(await self.start_calendar(new_year))
        if data['act'] == "START":
            await call.message.edit_reply_markup(await self.start_calendar(int(data['year'])))
        if data['act'] == "SET-MONTH":
            await call.message.edit_reply_markup(await self._get_days_kb(int(data['year']), int(data['month'])))
        if data['act'] == "SET-DAY":
            await call.message.edit_reply_markup(await self._get_hours_kb(
                int(data['year']), int(data['month']), int(data['day'])))  # removing inline keyboard
        if data['act'] == "SET-HOUR":
            await call.message.edit_reply_markup(await self._get_minutes_kb(
                int(data['year']), int(data['month']), int(data['day']), int(data['hour'])))
        if data['act'] == "SET-MINUTE":
            await call.message.delete_reply_markup()  # removing inline keyboard
            return_data = True, datetime(int(data['year']), int(data['month']), int(data['day']), int(data['hour']),
                                         int(data['minute']))
        return return_data
