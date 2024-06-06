from datetime import datetime
from operator import itemgetter

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram_dialog import DialogManager, Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Multiselect, Button
from aiogram_dialog.widgets.text import Format

from data.dates import days, hours, minutes, days_fullname_dict
from handlers.users.options import options_keyboard
from keyboards.inline.back_to_options_button import back_to_options_button_func


class Register(StatesGroup):
    hello = State()
    name = State()


class Sub(StatesGroup):
    text = State()


async def get_data(dialog_manager: DialogManager, **kwargs):
    # dialog_data = dialog_manager.current_context().dialog_data
    # print(dialog_data)
    updating_user_id = int(dialog_manager.current_context().start_data.get('updating_user_id'))


multiselect = Multiselect(
    checked_text=Format("✓ {item[0]}"), unchecked_text=Format("{item[0]}"),
    id="mselect",
    item_id_getter=itemgetter(2),
    items=days,
)


async def go_to_options(c: CallbackQuery, button: Button, manager: DialogManager):
    await options_keyboard(message=c)


async def get_all_checked(c: CallbackQuery, button: Button, manager: DialogManager):
    x = Multiselect.get_checked(multiselect, manager=manager)
    updating_user_id = int(manager.current_context().start_data.get('updating_user_id'))
    chosen_days = ", ".join(str(x) for index, x in enumerate(x))
    chosen_days_list = list(x)
    chosen_days_all = []
    for day in chosen_days_list:
        day = int(day)
        chosen_days_one = days_fullname_dict.get(day)
        chosen_days_all.append(chosen_days_one)
    chosen_days_all_string = ", ".join(str(chosen_days_all) for index, chosen_days_all in enumerate(chosen_days_all))
    markup = await choose_level_for_time_frequency(chosen_days, updating_user_id)
    await c.message.edit_reply_markup()
    await c.message.answer(f"Ви обрали наступні дні для нагадування:\n"
                           f"{chosen_days_all_string}.\n"
                           f"Для них оберіть час, у який ви хочете, щоб ми вам нагадали про тренування:",
                           reply_markup=markup)


back_button = Button(
    Format("Повернутись до опцій"),
    id="back",
    # back_button,
    on_click=go_to_options
)

get_all_checked_button = Button(
    Format("Обрати час нагадування"),
    id="got_all",
    # back_button,
    on_click=get_all_checked
)

make_schedule_dialog = Dialog(
    Window(
        Format(
            "Оберіть дні у які хочете отримувати нагадування в однаковий час.\n"
            "Якщо ви хочете отримувати нагадування в різний час зробіть інший розклад тренувань після вибору цього."
        ),
        multiselect,
        get_all_checked_button,
        back_button,
        state=Register.hello,
        getter=get_data,
    ),
)


async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Register.hello, mode=StartMode.RESET_STACK)


frequency_calendar_callback = CallbackData('frequency_calendar', 'act', 'chosen_days', 'updating_user_id', 'hour',
                                           'minute')
ignore_callback = frequency_calendar_callback.new("IGNORE", "chosen_days", 'updating_user_id', -1,
                                                  -1)  # for buttons with no answer


async def choose_level_for_time_frequency(chosen_days, updating_user_id):
    return await FrequencyCalendar()._get_hours_kb(chosen_days, updating_user_id)


class FrequencyCalendar:

    def __init__(self, hour: int = datetime.now().hour, minute: int = datetime.now().minute):
        self.hour = hour
        self.minute = minute

    async def _get_hours_kb(self, chosen_days, updating_user_id) -> InlineKeyboardMarkup:

        inline_kb = InlineKeyboardMarkup(row_width=6)
        inline_kb.row()
        for hour in hours:
            inline_kb.insert(InlineKeyboardButton(
                hour,
                callback_data=frequency_calendar_callback.new("SET-HOUR", chosen_days, updating_user_id, hour, -1)
            ))
        inline_button_options = await back_to_options_button_func()
        inline_kb.row()
        inline_kb.insert(inline_button_options)

        return inline_kb

    async def _get_minutes_kb(self, chosen_days, updating_user_id, hour: int):
        inline_kb = InlineKeyboardMarkup(row_width=6)
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            text=f"{hour}:",
            callback_data=frequency_calendar_callback.new("IGNORE", chosen_days, updating_user_id, -1, -1)
        ))
        inline_kb.row()
        for minute in minutes:
            inline_kb.insert(InlineKeyboardButton(
                minute,
                callback_data=frequency_calendar_callback.new("SET-MINUTE", chosen_days, updating_user_id, hour, minute)
            ))
        inline_button_options = await back_to_options_button_func()
        inline_kb.row()
        inline_kb.insert(inline_button_options)

        return inline_kb

    async def frequency_selection(self, call: CallbackQuery, data: CallbackData) -> tuple:
        return_data = (False, None)
        if data['act'] == "IGNORE":
            await call.answer(cache_time=5)
        if data['act'] == "SET-HOUR":
            await call.message.edit_reply_markup(
                await self._get_minutes_kb(str(data['chosen_days']), int(data['updating_user_id']), int(data['hour'])))
        if data['act'] == "SET-MINUTE":
            await call.message.delete_reply_markup()  # removing inline keyboard
            return_data = True, (
                str(data['chosen_days']), (int(data['updating_user_id'])), (int(data['hour']), int(data['minute'])))
        return return_data
