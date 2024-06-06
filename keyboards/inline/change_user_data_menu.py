from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import options_callback, \
    change_user_name_callback, change_user_timezone_callback, change_user_birthday_callback, change_user_sex_callback, \
    change_user_level_callback, change_user_sex_male_fem_no_callback, change_user_level_low_mid_high_callback


async def change_user_data_menu_func(updating_user_id):
    change_user_data_menu_func_kb = InlineKeyboardMarkup(row_width=1)
    change_user_data_menu_func_kb.row()
    change_user_data_menu_func_kb.insert(
        InlineKeyboardButton(text="Змінити ім'я",
                             callback_data=change_user_name_callback.new(updating_user_id=updating_user_id)))
    change_user_data_menu_func_kb.insert(
        InlineKeyboardButton(text="Змінити часовий пояс",
                             callback_data=change_user_timezone_callback.new(updating_user_id=updating_user_id)))
    change_user_data_menu_func_kb.insert(
        InlineKeyboardButton(text="Вказати день народження",
                             callback_data=change_user_birthday_callback.new(updating_user_id=updating_user_id)))
    change_user_data_menu_func_kb.insert(
        InlineKeyboardButton(text="Вказати стать",
                             callback_data=change_user_sex_callback.new(updating_user_id=updating_user_id)))
    change_user_data_menu_func_kb.insert(
        InlineKeyboardButton(text="Змінити рівень складності",
                             callback_data=change_user_level_callback.new(updating_user_id=updating_user_id)))
    change_user_data_menu_func_kb.insert(
        InlineKeyboardButton(text="Перейти до опцій", callback_data=options_callback.new(type="Callback")))
    return change_user_data_menu_func_kb


async def get_user_timezone_button_func(user_id):
    get_user_timezone_button_func_kb = InlineKeyboardMarkup(row_width=1)
    get_user_timezone_button_func_kb.row()
    get_user_timezone_button_func_kb.insert(
        InlineKeyboardButton(text="Вказати часовий пояс",
                             callback_data=change_user_timezone_callback.new(updating_user_id=user_id)))
    return get_user_timezone_button_func_kb


async def change_user_sex_menu_func():
    change_user_sex_menu_func_kb = InlineKeyboardMarkup(row_width=2)
    change_user_sex_menu_func_kb.row()
    change_user_sex_menu_func_kb.insert(
        InlineKeyboardButton(text="Чоловіча",
                             callback_data=change_user_sex_male_fem_no_callback.new(updating_user_id=1, sex="male")))
    change_user_sex_menu_func_kb.insert(
        InlineKeyboardButton(text="Жіноча",
                             callback_data=change_user_sex_male_fem_no_callback.new(updating_user_id=1, sex="female")))
    change_user_sex_menu_func_kb.insert(
        InlineKeyboardButton(text="Перейти до опцій", callback_data=options_callback.new(type="Callback")))
    return change_user_sex_menu_func_kb


async def change_level_menu_func():
    change_level_menu_func_kb = InlineKeyboardMarkup(row_width=1)
    change_level_menu_func_kb.row()
    change_level_menu_func_kb.insert(InlineKeyboardButton(text="Початковий рівень",
                                                          callback_data=change_user_level_low_mid_high_callback.new(
                                                              level="low")))
    change_level_menu_func_kb.insert(InlineKeyboardButton(text="Середній рівень",
                                                          callback_data=change_user_level_low_mid_high_callback.new(
                                                              level="medium")))
    change_level_menu_func_kb.insert(InlineKeyboardButton(text="Професіональний рівень",
                                                          callback_data=change_user_level_low_mid_high_callback.new(
                                                              level="high")))
    change_level_menu_func_kb.insert(
        InlineKeyboardButton(text="Перейти до опцій", callback_data=options_callback.new(type="Callback")))
    return change_level_menu_func_kb
