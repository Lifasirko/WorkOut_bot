import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_datas import start_workout_callback, workout_menu_callback, \
    pause_callback, finish_workout_callback, pause_between_sets_callback
from keyboards.inline.workout_menu import workout_menu, start_new_set, pause_workout_kb, \
    finish_workout_kb, pause_between_sets_kb
from loader import dp, bot
from utils.db_api import quick_commands as commands


@dp.callback_query_handler(start_workout_callback.filter())
async def start_workout_handler(call: CallbackQuery, callback_data: dict):
    ex_number = int(callback_data.get("ex_number"))
    workout = callback_data.get("workout_id")
    workout_id = int(workout)
    exercises = await commands.get_exercises_in_workout(workout_id)
    amount_of_exercises = len(exercises)

    if ex_number == 0:
        program = int(callback_data.get("program_id"))
        program_id = int(program)
        await commands.add_workout_history(user_id=call.from_user.id, program_id=program_id, workout_id=workout_id)

    if ex_number < amount_of_exercises:
        exercise = exercises[ex_number]
        exercise_id = exercise.exercise_id
        ex_number += 1
        exercise_name = await commands.get_exercise_name(exercise_id)
        exercise_file = await commands.get_exercise_file(exercise_id)
        exercise_description = await commands.get_exercise_description(exercise_id)
        exercise_file_type = await commands.get_exercise_file_type(exercise_id)
        a_o_s = await commands.get_exercise_sets(workout_id, exercise_id)
        amount_of_sets = int(a_o_s)
        # await call.answer(cache_time=5)
        set_number = 0
        exercise_repetitions = await commands.get_exercise_repetitions(workout_id=workout_id,
                                                                       exercise_id=exercise_id)
        markup = await workout_menu(user_id=call.from_user.id, workout_id=workout_id, exercise_id=exercise_id,
                                    ex_number=ex_number, set_number=set_number)

        if ex_number == 1:
            await call.message.edit_reply_markup()

            text = ("Вітаю з початком тренуванням!\n"
                    f"Ваша перша вправа:\n"
                    f"{ex_number}. {exercise_name}\n"
                    f"Опис вправи:\n"
                    f"{exercise_description}\n"
                    f"Кількість підходів - {amount_of_sets}\n"
                    f"Кількість повторів - {exercise_repetitions}")
        else:
            text = (f"Наступна вправа:\n"
                    f"{ex_number}. {exercise_name}\n"
                    f"Опис вправи:\n"
                    f"{exercise_description}\n"
                    f"Кількість підходів - {amount_of_sets}\n"
                    f"Кількість повторів - {exercise_repetitions}")
        if exercise_file_type == "animation":
            print(exercise_file_type)
            await bot.send_animation(chat_id=call.from_user.id, animation=exercise_file,
                                     caption=text,
                                     reply_markup=markup)
        elif exercise_file_type == "video":
            print(exercise_file_type)
            await bot.send_video(chat_id=call.from_user.id, video=exercise_file,
                                 caption=text,
                                 reply_markup=markup)
        # elif exercise_file_type == "document":
        #     await bot.send_animation(chat_id=call.from_user.id, animation=exercise_file,
        #                              caption=text,
        #                              reply_markup=markup)
        else:
            print(exercise_file_type)
            await bot.send_animation(chat_id=call.from_user.id, animation=exercise_file,
                                     caption=text,
                                     reply_markup=markup)
    else:
        await commands.make_workout_done(user_id=call.from_user.id, workout_id=workout_id)

        markup = await finish_workout_kb(user_id=call.from_user.id, workout_id=workout_id)
        await call.message.answer(text="Вітаю з завершенням тренування!\n"
                                       "Можете одразу запланувати наступне або ми нагадаємо вам завтра.",
                                  reply_markup=markup)


@dp.callback_query_handler(workout_menu_callback.filter(), state="*")
async def start_exercise_handler(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.finish()
    user_id = call.from_user.id
    workout_id = callback_data.get("workout_id")
    exercise_id = callback_data.get("exercise_id")
    set_number = int(callback_data.get("set_number"))
    ex_number = callback_data.get("ex_number")
    time_dependent = await commands.is_time_dependant(workout_id, exercise_id)
    a_o_s = await commands.get_exercise_sets(workout_id, exercise_id)
    amount_of_sets = int(a_o_s)
    exercise_repetitions = await commands.get_exercise_repetitions(workout_id=workout_id,
                                                                   exercise_id=exercise_id)
    exercise_duration = await commands.get_exercise_duration(exercise_id=exercise_id)
    repetition_duration = exercise_repetitions * exercise_duration
    await call.message.answer(f"Кількість підходів - {amount_of_sets}\n"
                              f"Номер підходу - {set_number}\n"
                              f"Кількість повторів - {exercise_repetitions}")
    exercises = await commands.get_exercises_in_workout(workout_id)
    amount_of_exercises = len(exercises)
    callback_data = {'@': 'start_day', 'workout_id': f'{workout_id}', 'ex_number': f'{ex_number}'}
    if int(ex_number) > amount_of_exercises:
        await start_workout_handler(call, callback_data)
    else:
        if time_dependent is True:
            await asyncio.sleep(repetition_duration)
            # await call.message.answer(text="Підхід завершено, відпочиньте 1 хвилину.")
            await pause_between_sets(call, callback_data)
        else:
            markup = await pause_between_sets_kb(user_id, workout_id, exercise_id, ex_number, set_number)
            await call.message.answer(text="Коли виконаєте всі повторення натисніть на кнопку знизу",
                                      reply_markup=markup)


@dp.callback_query_handler(pause_between_sets_callback.filter())
async def pause_between_sets(call: CallbackQuery, callback_data: dict):
    workout_id = callback_data.get("workout_id")
    exercise_id = callback_data.get("exercise_id")
    set_number = int(callback_data.get("set_number"))
    ex_number = callback_data.get("ex_number")
    from_call = callback_data.get("from_call")
    if from_call == "True":
        await call.message.edit_reply_markup()
    # callback_data = {'@': 'start_day', 'workout_id': f'{workout_id}', 'ex_number': f'{ex_number}'}
    a_o_s = await commands.get_exercise_sets(workout_id, exercise_id)
    amount_of_sets = int(a_o_s)

    markup = await start_new_set(user_id=call.from_user.id, workout_id=workout_id, exercise_id=exercise_id,
                                 ex_number=ex_number, set_number=set_number)
    if set_number < amount_of_sets:
        await call.message.answer(text="Підхід завершено, відпочиньте 1 хвилину.")
        await asyncio.sleep(4)
        await call.message.answer("Початок вправи через 15 секунд")
        await asyncio.sleep(1)
        await call.message.answer("3")
        await asyncio.sleep(1)
        await call.message.answer("2")
        await asyncio.sleep(1)
        await call.message.answer("1")
        await asyncio.sleep(1)
        await call.message.answer("Для початку наступного підходу натисніть Start!",
                                  reply_markup=markup)
    else:
        callback_data = {'@': 'start_day', 'workout_id': f'{workout_id}', 'ex_number': f'{ex_number}'}
        exercises = await commands.get_exercises_in_workout(workout_id)
        amount_of_exercises = len(exercises)
        if int(ex_number) < amount_of_exercises:
            await call.message.answer(text="Вітаю, ви завершили підходи цієї вправи! Переходимо до наступної!")
            await asyncio.sleep(2)
            await start_workout_handler(call, callback_data)
        else:
            await start_workout_handler(call, callback_data)


@dp.callback_query_handler(pause_callback.filter())
async def pause_workout_handler(call, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    workout_id = callback_data.get("workout_id")
    exercise_id = callback_data.get("exercise_id")
    ex_number = callback_data.get("ex_number")
    set_number = callback_data.get("set_number")
    markup = await pause_workout_kb(user_id=call.from_user.id, workout_id=workout_id, exercise_id=exercise_id,
                                    ex_number=ex_number, set_number=set_number)
    await call.message.answer(text="Ви вирішили взяти більшу перерву або припинити тренування?\n"
                                   "Якщо вам зле - дивіться не подохніть!!!",
                              reply_markup=markup)
    await state.set_state("pause")
    await asyncio.sleep(900)
    if await state.get_state() == "pause":
        await finish_workout(call, callback_data, state, user_id=call.from_user.id)


@dp.callback_query_handler(finish_workout_callback.filter(), state="*")
async def finish_workout(call: CallbackQuery, callback_data: dict, state: FSMContext, user_id: int = None):
    workout_id = int(callback_data.get("workout_id"))
    if user_id:
        user_id = user_id
        markup = await finish_workout_kb(user_id=user_id, workout_id=workout_id)

        await call.bot.edit_message_text(
            chat_id=int(user_id),
            text="Ви були відсутні більше 15 хвилин, через що тренування завершилось.\n"
                 "Наступного разу почнемо з нього.\n"
                 "Можете одразу запланувати наступне або ми нагадаємо вам завтра.",
            reply_markup=markup, message_id=call.message.message_id + 1
        )

    else:
        user_id = int(call.from_user.id)
        await call.message.edit_reply_markup()
        markup = await finish_workout_kb(user_id=user_id, workout_id=workout_id)

        await call.bot.send_message(chat_id=user_id,
                                    text="Ви завершили тренування. Наступного разу почнемо з нього.\n"
                                         "Можете одразу запланувати наступне або ми нагадаємо вам завтра.",
                                    reply_markup=markup)
    await state.finish()
