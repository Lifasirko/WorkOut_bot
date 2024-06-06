from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import options_callback, set_children_workout_callback, \
    get_children_statistics_callback, choose_children_callback, get_children_finish_workout_callback
from loader import dp
from utils.db_api import quick_commands as commands


async def children_menu_func(user_id, workout_id: int = None):
    bot_user = await dp.bot.get_me()

    children = await commands.get_user_children(referral_id=user_id)
    children_menu_func_kb = InlineKeyboardMarkup(row_width=1)
    children_menu_func_kb.row()
    children_menu_func_kb.insert(
        InlineKeyboardButton(text="Додати дитину",
                             switch_inline_query=f"http://t.me/{bot_user.username}?start=parent{user_id}"))
    for telegram_id, name, real_name in children:
        if real_name:
            child_name = real_name
        else:
            child_name = name
        children_menu_func_kb.insert(InlineKeyboardButton(
            text=f"{child_name}",
            callback_data=choose_children_callback.new(child_id=telegram_id, child_name=child_name)))
    children_menu_func_kb.insert(InlineKeyboardButton(text="Повернутися до опцій",
                                                      callback_data=options_callback.new(type="Callback")))
    return children_menu_func_kb


async def child_menu_func(child_id, child_name):
    child_menu_func_kb = InlineKeyboardMarkup(row_width=1)
    child_menu_func_kb.row()
    child_menu_func_kb.insert(InlineKeyboardButton(
        text="Налаштувати ранкову зарядку дитини",
        callback_data=set_children_workout_callback.new(child_id=child_id, child_name=child_name)))
    child_menu_func_kb.insert(InlineKeyboardButton(
        text="Переглянути статистику дитини",
        callback_data=get_children_statistics_callback.new(child_id=child_id)))
    child_menu_func_kb.insert(InlineKeyboardButton(
        text="Отримувати повідомлення про закінчення тренування",
        callback_data=get_children_finish_workout_callback.new(child_id=child_id)))
    child_menu_func_kb.insert(InlineKeyboardButton(text="Повернутися до опцій",
                                                   callback_data=options_callback.new(type="Callback")))

    return child_menu_func_kb
