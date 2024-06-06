from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hcode

from data.dates import days_eng_ukr_dict
from keyboards.inline.back_to_options_button import back_to_options_button
from keyboards.inline.calendar_menu import choose_date_callback, ChooseDate
from keyboards.inline.callback_datas import change_user_data_callback, change_user_name_callback, \
    change_user_birthday_callback, change_user_sex_callback, change_user_level_callback, \
    change_user_sex_male_fem_no_callback, change_user_level_low_mid_high_callback
from keyboards.inline.change_user_data_menu import change_user_sex_menu_func, change_level_menu_func, \
    change_user_data_menu_func
from loader import dp
from utils.db_api import quick_commands as commands


@dp.callback_query_handler(change_user_data_callback.filter())
async def change_user_data(call: CallbackQuery):
    updating_user_id = call.from_user.id
    markup = await change_user_data_menu_func(updating_user_id)
    await call.message.edit_reply_markup()
    await call.message.answer(text="Оберіть яку інформацію ви хочете додати чи змінити:",
                              reply_markup=markup)


@dp.callback_query_handler(change_user_name_callback.filter())
async def change_user_name(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer("Надішліть своє ім'я")
    await state.set_state("change_user_name")


@dp.message_handler(state="change_user_name")
async def enter_user_name(message: types.Message, state: FSMContext):
    real_name = message.text
    await commands.update_user_real_name(telegram_id=message.from_user.id, real_name=real_name)
    user = await commands.select_user(telegram_id=message.from_user.id)
    await message.answer("Дані оновлені. Запис в БД: \n" +
                         hcode(f"ім'я - {user.real_name}\n"), reply_markup=back_to_options_button)
    await state.finish()


@dp.callback_query_handler(change_user_birthday_callback.filter())
async def change_user_name(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    markup = await ChooseDate().start_calendar()
    await call.message.answer("Оберіть свою дату народження", reply_markup=markup)


@dp.callback_query_handler(choose_date_callback.filter())
async def process_dialog_calendar(call: CallbackQuery, callback_data: dict):
    selected, date = await ChooseDate().process_selection(call, callback_data)
    if selected:
        day = date.strftime("%A")
        day_to_user = days_eng_ukr_dict.get(day)
        # print(day_to_user)
        await commands.update_birthday(telegram_id=call.from_user.id, birthday=date)
        await call.message.answer(
            f'Ви народились {date.strftime("%d.%m.%Y")}.  До речі, цей день - {day_to_user}',
            reply_markup=back_to_options_button)


@dp.callback_query_handler(change_user_sex_callback.filter())
async def change_user_name(call: CallbackQuery):
    await call.message.edit_reply_markup()
    markup = await change_user_sex_menu_func()
    await call.message.answer("Оберіть свою стать", reply_markup=markup)


@dp.callback_query_handler(change_user_sex_male_fem_no_callback.filter())
async def enter_user_name(call: CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup()
    sex = callback_data.get("sex")
    await commands.update_sex(telegram_id=call.from_user.id, sex=sex)
    user = await commands.select_user(telegram_id=call.from_user.id)
    await call.message.answer("Дані оновлені. Запис в БД: \n" +
                              f"ваша стать - {user.sex}\n", reply_markup=back_to_options_button)


@dp.callback_query_handler(change_user_level_callback.filter())
async def change_user_name(call: CallbackQuery, state: FSMContext):
    markup = await change_level_menu_func()
    await call.message.answer("Оберіть рівень складності", reply_markup=markup)


@dp.callback_query_handler(change_user_level_low_mid_high_callback.filter())
async def enter_user_name(call: CallbackQuery, callback_data: dict):
    await call.message.edit_reply_markup()
    level = callback_data.get("level")
    await commands.update_level(telegram_id=call.from_user.id, level=level)
    user = await commands.select_user(telegram_id=call.from_user.id)
    await call.message.answer("Дані оновлені. Запис в БД: \n" +
                              hcode(f"ваш рівень складності - {user.level}\n"), reply_markup=back_to_options_button)
