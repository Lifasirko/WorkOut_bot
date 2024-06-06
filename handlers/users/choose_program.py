from loader import dp
from typing import Union

# import call as call
from aiogram.types import Message, CallbackQuery

from keyboards.inline.callback_datas import menu_cd, choose_program_callback
from keyboards.inline.choose_program_and_workout_menu import programs_keyboard, workout_keyboard, \
    back_to_workout_button, exercises_keyboard_or_start_workout
from utils.db_api import quick_commands as commands


# from keyboards.inline.choose_workout_menu import choose_workout_menu


@dp.callback_query_handler(choose_program_callback.filter())
# Та самая функция, которая отдает категории. Она может принимать как CallbackQuery, так и Message.
# Помимо этого, мы в нее можем отправить и другие параметры - category, subcategory, item_id,
# Поэтому ловим все остальное в **kwargs
async def list_programs(message: Union[CallbackQuery, Message], **kwargs):
    # Клавиатуру формируем с помощью следующей функции (где делается запрос в базу данных)
    markup = await programs_keyboard(user_id=message.from_user.id)

    # Проверяем, что за тип апдейта. Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        await message.answer("Оберіть програму тренування:", reply_markup=markup)

    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup()
        await call.message.answer(text="Оберіть програму тренування:", reply_markup=markup)
        # await call.message.edit_reply_markup(markup)


# Функция, которая отдает кнопки с подкатегориями, по выбранной пользователем категории
async def list_workouts(callback: CallbackQuery, program_id, **kwargs):
    markup = await workout_keyboard(program_id)

    await callback.message.edit_reply_markup()
    await callback.message.answer(text="Оберіть тренування:", reply_markup=markup)

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    # await callback.message.edit_reply_markup(markup)


# Функция, которая отдает кнопки с Названием и ценой товара, по выбранной категории и подкатегории
async def list_exercises(callback: CallbackQuery, program_id, workout_id, **kwargs):
    markup = await exercises_keyboard_or_start_workout(program_id, workout_id)
    await callback.message.edit_reply_markup()

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    await callback.message.answer(text="Хочете почати тренування або дізнатись більше про вправу?",
                                  reply_markup=markup)

    # await callback.message.edit_text # изменяет текст


# Функция, которая отдает уже кнопку "Купить" товар по выбранному товару
async def show_exercise(callback: CallbackQuery, program_id, workout_id, exercise_id):
    await callback.message.edit_reply_markup()
    markup = await back_to_workout_button(program_id, workout_id)

    # Берем запись о нашем товаре из базы данных
    exercise_name = await commands.get_exercise_name(exercise_id)
    exercise_file = await commands.get_exercise_file(exercise_id)
    exercise_description = await commands.get_exercise_description(exercise_id)
    text = (f"{exercise_name}\n"
            f"{exercise_description}")
    await callback.message.answer_animation(animation=exercise_file, caption=text, reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    program_id = callback_data.get("program_id")
    workout_id = callback_data.get("workout_id")
    exercise_id = callback_data.get("exercise_id")

    # Прописываем "уровни" в которых будут отправляться новые кнопки пользователю
    levels = {
        "0": list_programs,  # Отдаем категории
        "1": list_workouts,  # Отдаем подкатегории
        "2": list_exercises,  # Отдаем товары
        "3": show_exercise  # Предлагаем купить товар
    }

    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[current_level]

    # Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    await current_level_function(
        call,
        program_id=program_id,
        workout_id=workout_id,
        exercise_id=exercise_id
    )

