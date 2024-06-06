from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import ADMINS, COACHES
from keyboards.inline.callback_datas import payment_callback, get_description_callback, \
    choose_program_callback, workout_schedule_callback, change_user_data_callback, additional_options_callback, \
    options_callback, children_menu_callback, workout_settings_callback
from loader import dp


async def options_menu_func(user_id, workout_id: int = None):
    updating_user_id = user_id
    options_menu_func_kb = InlineKeyboardMarkup(row_width=1)
    options_menu_func_kb.row()
    num = 0
    allowed_users = []
    for user in ADMINS:
        int_user = int(user)
        allowed_users.insert(num, int_user)
        num += 1
    for user in COACHES:
        int_user = int(user)
        allowed_users.insert(num, int_user)
        num += 1
    if user_id in allowed_users:
        options_menu_func_kb.insert(
            InlineKeyboardButton(text="Налаштування тренувань", callback_data=workout_settings_callback.new(user_id)))
    options_menu_func_kb.insert(InlineKeyboardButton(text="Оплата", callback_data=payment_callback.new(id=1)))
    options_menu_func_kb.insert(InlineKeyboardButton(text="Додаткові налаштування",
                                                     callback_data=additional_options_callback.new(
                                                         type=1, updating_user_id=updating_user_id
                                                     )))
    options_menu_func_kb.insert(InlineKeyboardButton(
        text="Обрати програму тренування", callback_data=choose_program_callback.new(
            id=updating_user_id)))  # TODO:сделать продолжение тренировки, а не выбор
    return options_menu_func_kb


async def additional_options_menu_func(user_id, updating_user_id: int = None):
    bot_user = await dp.bot.get_me()
    if updating_user_id:
        updating_user_id = updating_user_id
    else:
        updating_user_id = user_id

    additional_options_menu_func_kb = InlineKeyboardMarkup(row_width=1)
    additional_options_menu_func_kb.row()
    additional_options_menu_func_kb.insert(InlineKeyboardButton(text="Змінити свої дані",
                                                                callback_data=change_user_data_callback.new(
                                                                    updating_user_id=updating_user_id)))
    additional_options_menu_func_kb.insert(InlineKeyboardButton(text="Налаштувати розклад тренувань",
                                                                callback_data=workout_schedule_callback.new(
                                                                    updating_user_id=updating_user_id)))
    additional_options_menu_func_kb.insert(InlineKeyboardButton(text="Обрати програму тренування",
                                                                callback_data=choose_program_callback.new(id=1)))
    additional_options_menu_func_kb.insert(
        InlineKeyboardButton(text="Надіслати запрошення",
                             # callback_data=get_referral_link_callback.new(id=1),
                             switch_inline_query=f"http://t.me/{bot_user.username}?start={user_id}"))
    additional_options_menu_func_kb.insert(InlineKeyboardButton(text="Меню дитячих тренувань",
                                                                callback_data=children_menu_callback.new(id=1)))
    additional_options_menu_func_kb.insert(InlineKeyboardButton(text="Опис програми",
                                                                callback_data=get_description_callback.new(id=1)))
    additional_options_menu_func_kb.insert(InlineKeyboardButton(text="Повернутися до опцій",
                                                                callback_data=options_callback.new(type="Callback")))
    return additional_options_menu_func_kb
