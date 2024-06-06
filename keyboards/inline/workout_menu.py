from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import pause_callback, workout_menu_callback, start_new_set_callback, \
    continue_workout_callback, finish_workout_callback, plan_next_workout_callback, options_callback, \
    pause_between_sets_callback


def make_callback_data_exercise(workout_id, exercise_id, ex_number, set_number):
    set_number = int(set_number)
    return workout_menu_callback.new(workout_id=workout_id, exercise_id=exercise_id, ex_number=ex_number,
                                     set_number=set_number + 1)


async def workout_menu(user_id, workout_id, exercise_id, ex_number, set_number):
    markup = InlineKeyboardMarkup(row_width=1)
    callback_data = make_callback_data_exercise(workout_id, exercise_id, ex_number, set_number)
    markup.row(InlineKeyboardButton(text="Розпочати вправу", callback_data=callback_data))
    markup.insert(InlineKeyboardButton(text="Взяти перерву",
                                       callback_data=pause_callback.new(workout_id, exercise_id, ex_number,
                                                                        set_number)))
    return markup


async def start_new_set(user_id, workout_id, exercise_id, ex_number, set_number):
    markup = InlineKeyboardMarkup(row_width=1)
    callback_data = make_callback_data_exercise(workout_id, exercise_id, ex_number, set_number)
    markup.row(InlineKeyboardButton(text="Start!", callback_data=callback_data))
    markup.insert(InlineKeyboardButton(text="Взяти перерву",
                                       callback_data=pause_callback.new(workout_id, exercise_id, ex_number,
                                                                        set_number)))
    return markup


async def pause_between_sets_kb(user_id, workout_id, exercise_id, ex_number, set_number, from_call=True):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(InlineKeyboardButton(text="Підхід виконано",
                                    callback_data=pause_between_sets_callback.new(workout_id, exercise_id, ex_number,
                                                                                  set_number, from_call)))
    markup.insert(InlineKeyboardButton(text="Взяти перерву",
                                       callback_data=pause_callback.new(workout_id, exercise_id, ex_number,
                                                                        set_number)))
    return markup


async def pause_workout_kb(user_id, workout_id, exercise_id, ex_number, set_number):
    markup = InlineKeyboardMarkup(row_width=1)
    s_n = int(set_number) - 1
    callback_data = make_callback_data_exercise(workout_id, exercise_id, ex_number, set_number=s_n)
    markup.row(InlineKeyboardButton(text="Продовжити тренування", callback_data=callback_data))
    markup.insert(InlineKeyboardButton(text="Завершити тренування",
                                       callback_data=finish_workout_callback.new(workout_id, exercise_id, set_number)))
    return markup


async def finish_workout_kb(user_id, workout_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(InlineKeyboardButton(text="Запланувати тренування",
                                    callback_data=plan_next_workout_callback.new(user_id, workout_id)))
    markup.insert(
        InlineKeyboardButton(text="Повернутись до опцій", callback_data=options_callback.new(type="Callback")))
    return markup
