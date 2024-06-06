import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import ADMINS
from data.set_dataclasses import Set_program, Set_exercise
from keyboards.inline.callback_datas import workout_settings_callback, add_new_program_callback, \
    set_program_access_callback, set_program_is_morning_callback, set_program_level_callback, \
    set_program_sex_callback, set_program_age_callback, add_new_workout_callback, add_new_exercise_callback, \
    program_settings_choose_set_callback, workout_settings_choose_set_callback, exercise_settings_choose_set_callback, \
    change_exercise_callback
from keyboards.inline.programs_settings_menu import workout_settings_options_menu_func, \
    set_program_access_callback_menu_func, \
    set_program_morning_workout_callback_menu_func, set_program_sex_callback_menu_func, \
    set_program_level_callback_menu_func, set_program_age_callback_menu_func, finish_settings, \
    settings_for_programs_menu_func, settings_for_workouts_menu_func, settings_for_exercises_menu_func, \
    choose_exercise_to_change_menu_func
from loader import dp, bot
from utils.db_api import quick_commands as commands


# ____________________________________________ Загальне меню редагування ____________________________________________ #


@dp.callback_query_handler(workout_settings_callback.filter())
async def programs_settings_commands(call: CallbackQuery, callback_data: dict):
    if str(call.from_user.id) in ADMINS:
        await call.message.edit_reply_markup()
        user_id = int(callback_data.get('user_id'))
        markup = await workout_settings_options_menu_func(user_id=user_id)
        await call.message.answer("Що ви хочете зробити?", reply_markup=markup)
    else:
        await call.message.answer("Ви не можете користуватись цією командою")


# _____________________________________________ Меню редагування програм _____________________________________________ #


@dp.callback_query_handler(program_settings_choose_set_callback.filter())
async def program_settings_choose_set(call: CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    markup = await settings_for_programs_menu_func(user_id)
    await call.message.answer("Що ви хочете зробити з програмою?", reply_markup=markup)


@dp.callback_query_handler(add_new_program_callback.filter())
async def add_new_program(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = int(callback_data.get('user_id'))
    last_program_id = await commands.get_last_program_id()
    program_id = last_program_id + 1
    result = await commands.create_new_program(program_id)
    await commands.set_program_creator(program_id, user_id)
    if result == "success":
        await call.message.answer("Напишіть назву програми")
        await Set_program.program_name.set()
        await state.set_data(program_id)
    else:
        markup = await workout_settings_options_menu_func(user_id)
        await call.message.answer("Виникла якась помилка. Зверніться до адміністратора чи спробуйте знову.",
                                  reply_markup=markup)


@dp.message_handler(state=Set_program.program_name)
async def enter_program_name(message: types.Message, state: FSMContext):
    program_id = await state.get_data("program_id")
    user_id = message.from_user.id
    program_name = message.text
    await commands.set_program_name(program_id, program_name)
    markup = await set_program_access_callback_menu_func(user_id, program_id)
    await message.answer(text=f"id програми - {program_id}\n"
                              f"Назва програми - {program_name}\n"
                              f"Програма безкоштовна?", reply_markup=markup)
    await Set_program.next()


@dp.callback_query_handler(set_program_access_callback.filter(), state="*")
async def set_program_access(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    access = callback_data.get("access")
    program_id = await state.get_data("program_id")
    await commands.set_program_access(program_id, access)
    markup = await set_program_morning_workout_callback_menu_func(user_id, program_id)
    text_free = f"Програма безкоштовна.\n" \
                f"Це ранкова програма?"
    text_paid = f"Програма платна, ціна - \n" \
                f"Це ранкова програма?"
    await call.message.answer(text=f"Це ранкова програма?\n"
                                   f"{access}", reply_markup=markup)
    await Set_program.next()


@dp.callback_query_handler(set_program_is_morning_callback.filter(), state="*")
async def set_program_access(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    morning = callback_data.get("morning")
    program_id = await state.get_data("program_id")
    await commands.set_program_morning(program_id, morning)
    markup = await set_program_level_callback_menu_func(user_id, program_id)
    await call.message.answer(text=f"Це ранкова програма - {morning}\n"
                                   f"Який рівень цієї програми?", reply_markup=markup)
    await Set_program.next()


@dp.callback_query_handler(set_program_level_callback.filter(), state="*")
async def set_program_access(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    level = callback_data.get("level")
    program_id = await state.get_data("program_id")
    await commands.set_program_level(program_id, level)
    markup = await set_program_sex_callback_menu_func(user_id, program_id)
    await call.message.answer(text=f"Рівень програми - {level}\n"
                                   f"Це програма для певної статі?", reply_markup=markup)
    await Set_program.next()


@dp.callback_query_handler(set_program_sex_callback.filter(), state="*")
async def set_program_access(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    sex = callback_data.get("sex")
    program_id = await state.get_data("program_id")
    await commands.set_program_sex(program_id, sex)

    markup = await set_program_age_callback_menu_func(user_id, program_id)
    await call.message.answer(text=f"Ця програма для {sex} статі.\n"
                                   f"Це програма для певного віку?", reply_markup=markup)
    await Set_program.next()


@dp.callback_query_handler(set_program_age_callback.filter(), state="*")
async def finish_creating_program(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    age = callback_data.get("age")
    program_id = await state.get_data("program_id")
    program_name = await commands.get_program_name(program_id)
    program_is_free = await commands.get_program_is_free(program_id)
    morning_program = await commands.get_morning_program(program_id)
    level_program = await commands.get_level_program(program_id)
    sex_program = await commands.get_sex_program(program_id)
    creator = await commands.get_creator(program_id)
    await commands.set_program_age(program_id, age)
    markup = await workout_settings_options_menu_func(user_id=user_id)
    await call.message.answer(text=f"Програма повністю створена!\n"
                                   f"id - {program_id}\n"
                                   f"Назва - {program_name}\n"
                                   f"Програма платна - {program_is_free}\n"
                                   f"Це ранкова програма - {morning_program}\n"
                                   f"Рівень складності програми - {level_program}\n"
                                   f"Програма для певної статі - {sex_program}\n"
                                   f"Програма для певного віку - {age}"
                                   f"Програму створив - {creator}",
                              reply_markup=markup)
    await state.finish()


# ____________________________________________ Меню редагування тренувань ____________________________________________ #

@dp.callback_query_handler(workout_settings_choose_set_callback.filter())
async def workout_settings_choose_set(call: CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    markup = await settings_for_workouts_menu_func(user_id)
    await call.message.answer("Що ви хочете зробити з тренуванням?", reply_markup=markup)


@dp.callback_query_handler(add_new_workout_callback.filter())
async def add_new_workout(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    last_workout_id = await commands.get_last_workout_id()
    workout_id = last_workout_id + 1
    result = await commands.create_new_workout(workout_id)
    if result == "success":
        await call.message.answer("Напишіть назву тренування")
        await state.set_state("workout_name")
        await state.set_data(workout_id)
    else:
        markup = await workout_settings_options_menu_func(user_id)
        await call.message.answer("Виникла якась помилка. Зверніться до адміністратора чи спробуйте знову.",
                                  reply_markup=markup)


@dp.message_handler(state="workout_name")
async def set_workout_name(message: types.Message, state: FSMContext):
    workout_id = await state.get_data("workout_id")
    user_id = message.from_user.id
    workout_name = message.text
    await commands.set_workout_name(workout_id, workout_name)
    markup = await workout_settings_options_menu_func(user_id=user_id)
    await message.answer(text=f"Ви створили тренування!\n"
                              f"id - {workout_id}\n"
                              f"Назва - {workout_name}", reply_markup=markup)
    await state.finish()


# ______________________________________________ Меню редагування вправ ______________________________________________ #


@dp.callback_query_handler(exercise_settings_choose_set_callback.filter())
async def exercise_settings_choose_set(call: CallbackQuery):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    markup = await settings_for_exercises_menu_func(user_id)
    await call.message.answer("Що ви хочете зробити з вправою?", reply_markup=markup)


@dp.callback_query_handler(add_new_exercise_callback.filter())
async def add_new_exercise(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    last_exercise_id = await commands.get_last_exercise_id()
    exercise_id = last_exercise_id + 1
    result = await commands.create_new_exercise(exercise_id)
    if result == "success":
        await call.message.answer("Напишіть назву тренування")
        await Set_exercise.exercise_name.set()
        # await state.set_state("exercise_name")
        await state.set_data(exercise_id)
    else:
        markup = await workout_settings_options_menu_func(user_id)
        await call.message.answer("Виникла якась помилка. Зверніться до адміністратора чи спробуйте знову.",
                                  reply_markup=markup)


@dp.message_handler(state=Set_exercise.exercise_name)
async def set_exercise_name(message: types.Message, state: FSMContext):
    exercise_id = await state.get_data("exercise_id")
    user_id = message.from_user.id
    exercise_name = message.text
    await commands.set_exercise_name(exercise_id, exercise_name)
    await message.answer(text=f"id - {exercise_id}\n"
                              f"Назва вправи - {exercise_name}\n"
                              f"Напишіть тривалість вправи у секундах (цифрами)")
    await Set_exercise.next()


@dp.message_handler(state=Set_exercise.exercise_duration)
async def set_exercise_duration(message: types.Message, state: FSMContext):
    exercise_id = await state.get_data("exercise_id")
    user_id = message.from_user.id
    exercise_duration = message.text
    await commands.set_exercise_duration(exercise_id, exercise_duration)
    await message.answer(text=f"id - {exercise_id}\n"
                              f"Тривалість вправи - {exercise_duration} секунд.\n"
                              f"Напишіть опис до вашої вправи")
    await Set_exercise.next()


@dp.message_handler(state=Set_exercise.exercise_definition)
async def set_exercise_definition(message: types.Message, state: FSMContext):
    exercise_id = await state.get_data("exercise_id")
    user_id = message.from_user.id
    exercise_definition = message.text
    await commands.set_exercise_definition(exercise_id, exercise_definition)
    await message.answer(text=f"id - {exercise_id}\n"
                              f"Опис вправи - {exercise_definition}\n"
                              f"Надішліть файл для вашої вправи")
    await Set_exercise.next()


@dp.message_handler(content_types=types.ContentType.ANIMATION, state=Set_exercise.exercise_file)
async def set_exercise_file(message: types.Message, state: FSMContext):
    exercise_id = await state.get_data("exercise_id")
    user_id = message.from_user.id
    exercise_file = message.animation.file_id
    exercise_file_type = "animation"
    await commands.set_exercise_file(exercise_id, exercise_file, exercise_file_type)
    await finish_set_exercise(message, state, user_id)


@dp.message_handler(content_types=types.ContentType.VIDEO, state=Set_exercise.exercise_file)
async def set_exercise_file(message: types.Message, state: FSMContext):
    exercise_id = await state.get_data("exercise_id")
    user_id = message.from_user.id
    exercise_file = message.animation.file_id
    exercise_file_type = "video"
    await commands.set_exercise_file(exercise_id, exercise_file, exercise_file_type)
    await finish_set_exercise(message, state, user_id)


@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=Set_exercise.exercise_file)
async def set_exercise_file(message: types.Message, state: FSMContext):
    exercise_id = await state.get_data("exercise_id")
    user_id = message.from_user.id
    exercise_file = message.animation.file_id
    exercise_file_type = "document"
    await commands.set_exercise_file(exercise_id, exercise_file, exercise_file_type)
    await finish_set_exercise(message, state, user_id)


async def finish_set_exercise(message: types.Message, state: FSMContext, user_id):
    exercise_id = await state.get_data("exercise_id")
    exercise_file = await commands.get_exercise_file(exercise_id)
    exercise_name = await commands.get_exercise_name(exercise_id)
    exercise_file_animation = await commands.get_exercise_file(exercise_id)
    exercise_description = await commands.get_exercise_description(exercise_id)
    exercise_duration = await commands.get_exercise_duration(exercise_id=exercise_id)
    await message.answer(text=f"id вправи - {exercise_id}\n"
                              f"Назва вправи - {exercise_name}\n"
                              f"id файлу - {exercise_file}\n"
                              f"Опис вправи:\n"
                              f"{exercise_description}\n"
                              f"\n"
                              f"Тривалість вправи - {exercise_duration}\n"
                              f"Ваша вправа буде виглядати так:")

    await asyncio.sleep(5)
    markup = await finish_settings(user_id)
    await bot.send_animation(chat_id=message.from_user.id, animation=exercise_file_animation,
                             caption=exercise_description, reply_markup=markup)
    await state.finish()


@dp.callback_query_handler(change_exercise_callback.filter())
async def choose_exercise_to_change(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    markup = await choose_exercise_to_change_menu_func(user_id=call.from_user.id)
    await call.message.answer("Оберіть програму, яку хочете змінити", reply_markup=markup)



