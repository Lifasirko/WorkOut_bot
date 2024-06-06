from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import menu_cd, start_workout_callback, options_callback
from utils.db_api import quick_commands as commands


# С помощью этой функции будем формировать callback_data для каждого элемента меню, в зависимости от
# переданных параметров. Если Подкатегория, или id товара не выбраны - они по умолчанию равны нулю
def make_callback_data(level, program_id=0, workout_id=0, exercise_id=0):
    return menu_cd.new(level=level, program_id=program_id, workout_id=workout_id, exercise_id=exercise_id)


def make_callback_data_start_workout(program_id, workout_id):
    return start_workout_callback.new(program_id=program_id, workout_id=workout_id, ex_number=0)


# Создаем функцию, которая отдает клавиатуру с доступными программами
async def programs_keyboard(user_id):
    # Указываем, что текущий уровень меню - 0
    CURRENT_LEVEL = 0

    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup(row_width=1)

    # Забираем список товаров из базы данных с РАЗНЫМИ категориями и проходим по нему
    programs = await commands.get_available_programs(user_id=user_id)
    for program in programs:
        # Чекаем в базе сколько товаров существует под данной категорией
        number_of_workouts_in_program = await commands.count_workouts_in_program(program_id=program.program_id)
        program_name = await commands.get_program_name(program_id=program.program_id)

        # Сформируем текст, который будет на кнопке
        button_text = f"{program_name}, {number_of_workouts_in_program} тренувань."

        # Сформируем callback_data, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, program_id=program.program_id)

        # Вставляем кнопку в клавиатуру
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.insert(
        InlineKeyboardButton(text="Повернутись до опцій", callback_data=options_callback.new(type="Callback")))
    # Возвращаем созданную клавиатуру в handler
    return markup


# Создаем функцию, которая отдает клавиатуру с доступными подкатегориями, исходя из выбранной категории
async def workout_keyboard(program_id):
    # Текущий уровень - 1
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)

    # Забираем список товаров с РАЗНЫМИ подкатегориями из базы данных с учетом выбранной категории и проходим по ним
    workouts = await commands.get_workouts_in_program(program_id=program_id)
    for workout in workouts:
        # Чекаем в базе сколько товаров существует под данной подкатегорией
        number_of_exercises = await commands.count_exercises_in_workout(workout_id=workout.workout_id)

        workout_name = await commands.get_workout_name(workout_id=workout.workout_id)

        # Сформируем текст, который будет на кнопке
        button_text = f"{workout_name} ({number_of_exercises} вправ)"

        # Сформируем callback_data, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           program_id=program_id, workout_id=workout.workout_id)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Создаем Кнопку "Назад", в которой прописываем callback_data. callback_data, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1))
    )
    return markup


# Создаем функцию, которая отдает клавиатуру с доступными товарами, исходя из выбранной категории и подкатегории
async def exercises_keyboard_or_start_workout(program_id, workout_id):
    CURRENT_LEVEL = 2

    # Устанавливаю row_width = 1, чтобы показывалась одна кнопка в строке на товар
    markup = InlineKeyboardMarkup(row_width=1, )

    markup.row(
        InlineKeyboardButton(
            text="🏋️ ПОЧАТИ ТРЕНУВАННЯ! 🏋️",
            callback_data=make_callback_data_start_workout(program_id=program_id, workout_id=workout_id)
        )
    )

    # Забираем список товаров из базы данных с выбранной категорией и подкатегорией, и проходим по нему
    exercises = await commands.get_exercises_in_workout(workout_id)
    for exercise in exercises:
        exercise_name = await commands.get_exercise_name(exercise_id=exercise.exercise_id)
        exercise_sets = await commands.get_exercise_sets(workout_id=workout_id, exercise_id=exercise.exercise_id)
        exercise_repetitions = await commands.get_exercise_repetitions(workout_id=workout_id,
                                                                       exercise_id=exercise.exercise_id)
        # Сформируем текст, который будет на кнопке
        button_text = f"{exercise_name} - {exercise_sets} сетів, {exercise_repetitions} повторень"

        # Сформируем callback_data, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           program_id=program_id, workout_id=workout_id,
                                           exercise_id=exercise.exercise_id)
        markup.insert(
            InlineKeyboardButton(
                text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(
            text="🏋️ ПОЧАТИ ТРЕНУВАННЯ! 🏋️",
            callback_data=make_callback_data_start_workout(program_id=program_id, workout_id=workout_id)
        )
    )

    # Создаем Кнопку "Назад", в которой прописываем callback_data. callback_data, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             program_id=program_id))
    )
    return markup


async def back_to_workout_button(program_id, workout_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=2,
                                             program_id=program_id, workout_id=workout_id))
    )
    return markup
