from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.set_dataclasses import level_program_eng_ukr, age2, sex
from keyboards.inline.callback_datas import options_callback, change_program_callback, \
    add_new_program_callback, set_program_access_callback, set_program_is_morning_callback, set_program_back_callback, \
    set_program_level_callback, set_program_age_callback, add_new_workout_callback, change_workout_callback, \
    add_new_exercise_callback, change_exercise_callback, workout_settings_callback, change_workout_exercise_callback, \
    change_program_workout_callback, program_settings_choose_set_callback, workout_settings_choose_set_callback, \
    exercise_settings_choose_set_callback, choose_exercise_to_change_callback
from utils.db_api import quick_commands as commands



async def workout_settings_options_menu_func(user_id):
    workout_settings_options_menu_func_kb = InlineKeyboardMarkup(row_width=1)
    workout_settings_options_menu_func_kb.row()
    workout_settings_options_menu_func_kb.insert(
        InlineKeyboardButton(text="Редагувати програми",
                             callback_data=program_settings_choose_set_callback.new(user_id=user_id)))
    workout_settings_options_menu_func_kb.insert(
        InlineKeyboardButton(text="Редагувати тренування",
                             callback_data=workout_settings_choose_set_callback.new(user_id=user_id)))
    workout_settings_options_menu_func_kb.insert(
        InlineKeyboardButton(text="Редагувати вправи",
                             callback_data=exercise_settings_choose_set_callback.new(user_id=user_id)))
    workout_settings_options_menu_func_kb.row()
    workout_settings_options_menu_func_kb.insert(
        InlineKeyboardButton(text="Повернутися до опцій",
                             callback_data=options_callback.new(type="Callback")))
    return workout_settings_options_menu_func_kb


async def settings_for_exercises_menu_func(user_id):
    settings_for_exercises_menu_func_kb = InlineKeyboardMarkup(row_width=1)
    settings_for_exercises_menu_func_kb.insert(
        InlineKeyboardButton(text="Створити нову вправу",
                             callback_data=add_new_exercise_callback.new(user_id=user_id)))
    settings_for_exercises_menu_func_kb.insert(
        InlineKeyboardButton(text="Редагувати існуючі вправи",
                             callback_data=change_exercise_callback.new(user_id=user_id)))
    settings_for_exercises_menu_func_kb.insert(
        InlineKeyboardButton(text="Повернутися до опцій",
                             callback_data=options_callback.new(type="Callback")))
    return settings_for_exercises_menu_func_kb


async def choose_exercise_to_change_menu_func(user_id):
    choose_exercise_to_change_menu_func_kb = InlineKeyboardMarkup(row_width=4)
    exercises = await commands.get_exercises_id()
    for exercise in exercises:
        exercise_id = exercise.exercise_id
        exercise_name = await commands.get_exercise_name(exercise_id)

        choose_exercise_to_change_menu_func_kb.insert(
            InlineKeyboardButton(text=exercise_id, callback_data=choose_exercise_to_change_callback.new(
                user_id=user_id, exercise_id=exercise_id
            )))
    return choose_exercise_to_change_menu_func_kb


async def settings_for_workouts_menu_func(user_id):
    settings_for_workouts_menu_func_kb = InlineKeyboardMarkup(row_width=1)
    settings_for_workouts_menu_func_kb.insert(
        InlineKeyboardButton(text="Створити нове тренування",
                             callback_data=add_new_workout_callback.new(user_id=user_id)))
    settings_for_workouts_menu_func_kb.insert(
        InlineKeyboardButton(text="Редагувати існуючі тренування",
                             callback_data=change_workout_callback.new(user_id=user_id)))
    settings_for_workouts_menu_func_kb.insert(
        InlineKeyboardButton(text="Редагувати тренування-вправи",
                             callback_data=change_workout_exercise_callback.new(user_id=user_id)))
    settings_for_workouts_menu_func_kb.insert(
        InlineKeyboardButton(text="Повернутися до опцій",
                             callback_data=options_callback.new(type="Callback")))
    return settings_for_workouts_menu_func_kb


async def settings_for_programs_menu_func(user_id):
    settings_for_programs_menu_func_kb = InlineKeyboardMarkup(row_width=1)
    settings_for_programs_menu_func_kb.insert(
        InlineKeyboardButton(text="Створити нову програму",
                             callback_data=add_new_program_callback.new(user_id=user_id)))
    settings_for_programs_menu_func_kb.insert(
        InlineKeyboardButton(text="Редагувати існуючі програми",
                             callback_data=change_program_callback.new(user_id=user_id)))
    settings_for_programs_menu_func_kb.insert(
        InlineKeyboardButton(text="Редагувати програми-тренування",
                             callback_data=change_program_workout_callback.new(user_id=user_id)))
    settings_for_programs_menu_func_kb.insert(
        InlineKeyboardButton(text="Повернутися до опцій",
                             callback_data=options_callback.new(type="Callback")))
    return settings_for_programs_menu_func_kb


async def add_new_program_callback_menu_func(user_id, program_id):
    add_new_program_callback_menu_func_kb = InlineKeyboardMarkup(row_width=2)
    add_new_program_callback_menu_func_kb.row()
    add_new_program_callback_menu_func_kb.insert(
        InlineKeyboardButton(text="Так",
                             callback_data=set_program_access_callback.new(user_id=user_id, program_id=program_id,
                                                                           access="True"))
    )
    add_new_program_callback_menu_func_kb.insert(
        InlineKeyboardButton(text="Ні",
                             callback_data=set_program_access_callback.new(user_id=user_id, program_id=program_id,
                                                                           access="False"))
    )
    add_new_program_callback_menu_func_kb.insert(
        InlineKeyboardButton(text="Повернутись назад",
                             callback_data=set_program_back_callback.new(user_id=user_id, program_id=program_id))
    )
    return add_new_program_callback_menu_func_kb


async def set_program_access_callback_menu_func(user_id, program_id):
    set_program_access_callback_menu_func_kb = InlineKeyboardMarkup(row_width=2)
    set_program_access_callback_menu_func_kb.row()
    set_program_access_callback_menu_func_kb.insert(
        InlineKeyboardButton(text="Так",  # TODO: продолжение с указание цены программы
                             callback_data=set_program_access_callback.new(user_id, program_id, access=True))
    )
    set_program_access_callback_menu_func_kb.insert(
        InlineKeyboardButton(text="Ні",
                             callback_data=set_program_access_callback.new(user_id, program_id, access=False))
    )
    set_program_access_callback_menu_func_kb.row()
    set_program_access_callback_menu_func_kb.insert(
        InlineKeyboardButton(text="Повернутись назад",
                             callback_data=set_program_back_callback.new(user_id, program_id))
    )
    return set_program_access_callback_menu_func_kb


async def set_program_morning_workout_callback_menu_func(user_id, program_id):
    set_program_morning_workout_callback_menu_func_kb = InlineKeyboardMarkup(row_width=2)
    set_program_morning_workout_callback_menu_func_kb.row()
    set_program_morning_workout_callback_menu_func_kb.insert(
        InlineKeyboardButton(text="Так",
                             callback_data=set_program_is_morning_callback.new(user_id, program_id, morning=True))
    )
    set_program_morning_workout_callback_menu_func_kb.insert(
        InlineKeyboardButton(text="Ні",
                             callback_data=set_program_is_morning_callback.new(user_id, program_id, morning=False))
    )
    set_program_morning_workout_callback_menu_func_kb.row()
    set_program_morning_workout_callback_menu_func_kb.insert(
        InlineKeyboardButton(text="Повернутись назад",
                             callback_data=set_program_back_callback.new(user_id, program_id))
    )
    return set_program_morning_workout_callback_menu_func_kb


async def set_program_level_callback_menu_func(user_id, program_id):
    set_program_level_callback_menu_func_kb = InlineKeyboardMarkup(row_width=2)
    set_program_level_callback_menu_func_kb.row()
    for key, value in level_program_eng_ukr.items():
        set_program_level_callback_menu_func_kb.insert(
            InlineKeyboardButton(text=value,
                                 callback_data=set_program_level_callback.new(user_id, program_id, level=key))
        )
    set_program_level_callback_menu_func_kb.insert(
        InlineKeyboardButton(text="Повернутись назад",
                             callback_data=set_program_back_callback.new(user_id, program_id))
    )
    return set_program_level_callback_menu_func_kb


async def set_program_sex_callback_menu_func(user_id, program_id):
    set_program_sex_callback_menu_func_kb = InlineKeyboardMarkup(row_width=2)
    set_program_sex_callback_menu_func_kb.row()  # TODO: сделать через цикл и словарь как с уровнем
    for key, value in sex.items():
        set_program_sex_callback_menu_func_kb.insert(
            InlineKeyboardButton(text=value,
                                 callback_data=set_program_age_callback.new(user_id, program_id, age=key))
        )

    # set_program_sex_callback_menu_func_kb.insert(
    #     InlineKeyboardButton(text="Чоловіча",
    #                          callback_data=set_program_sex_callback.new(user_id, program_id, sex="male"))
    # )
    # set_program_sex_callback_menu_func_kb.insert(
    #     InlineKeyboardButton(text="Жіноча",
    #                          callback_data=set_program_sex_callback.new(user_id, program_id, sex="female"))
    # )
    # set_program_sex_callback_menu_func_kb.row()
    # set_program_sex_callback_menu_func_kb.insert(
    #     InlineKeyboardButton(text="Будь-яка стать",
    #                          callback_data=set_program_sex_callback.new(user_id, program_id, sex="None"))
    # )
    set_program_sex_callback_menu_func_kb.insert(
        InlineKeyboardButton(text="Повернутись назад",
                             callback_data=set_program_back_callback.new(user_id, program_id))
    )
    return set_program_sex_callback_menu_func_kb


async def set_program_age_callback_menu_func(user_id, program_id):
    set_program_age_callback_menu_func_kb = InlineKeyboardMarkup(row_width=2)
    set_program_age_callback_menu_func_kb.row()
    for key, value in age2.items():
        set_program_age_callback_menu_func_kb.insert(
            InlineKeyboardButton(text=value,
                                 callback_data=set_program_age_callback.new(user_id, program_id, age=key))
        )
    set_program_age_callback_menu_func_kb.insert(
        InlineKeyboardButton(text="Повернутись назад",
                             callback_data=set_program_back_callback.new(user_id, program_id))
    )
    return set_program_age_callback_menu_func_kb


# async def set_program_back_callback():


async def finish_settings(user_id):
    set_workout_name_menu_func_kb = InlineKeyboardMarkup(row_width=2)
    set_workout_name_menu_func_kb.row()
    set_workout_name_menu_func_kb.insert(
        InlineKeyboardButton(
            text="Завершити редагування", callback_data=workout_settings_callback.new(user_id)
        )
    )
