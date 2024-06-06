from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

# from aiogram.utils.markdown import hcode
from data.child_morning_workout import child_morning_workout
from data.config import ADMINS
from data.exercises_by_ivan_adamov import exercises_by_ivan_adamov
from data.exercises_paul_wade import exercises_paul_wade
from loader import dp
from utils.db_api import quick_commands as commands


@dp.message_handler(Command("email"))
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer("Пришли мне свой e-mail")
    await state.set_state("email")


# @dp.message_handler(state="email")
# async def enter_email(message: types.Message, state: FSMContext):
#     email = message.text
#     await commands.update_user_email(email=email, id=message.from_user.id)
#     user = await commands.select_user(id=message.from_user.id)
#     await message.answer("Данные обновлены. Запись в БД: \n" +
#                          hcode(f"id={user.id}\n"
#                                f"name={user.name}\n"
#                                f"email={user.email}"))
#     await state.finish()


@dp.message_handler(Command("update_db"))
async def update_db(
        # message: types.Message
):
    await commands.add_user(telegram_id=1)
    await commands.add_program(program_id=1, program_name="Ранкова зарядка для дітей", program_is_free=True,
                               morning_program=True, level_program="any", age_program="Дитяча")
    await commands.add_program(program_id=2, program_name="Свежая кровь", program_is_free=True, morning_program=False)
    await commands.add_program(program_id=3, program_name="Хорошее поведение", program_is_free=True,
                               morning_program=False)
    await commands.add_program(program_id=4, program_name="exercises_by_ivan_adamov", program_is_free=True,
                               morning_program=False)

    await commands.add_workout(workout_id=1, workout_name="Понеділок", workout_frequency=1)
    await commands.add_workout(workout_id=2, workout_name="Понедельник 1", workout_frequency=1)
    await commands.add_workout(workout_id=3, workout_name="Вторник 1", workout_frequency=1)
    await commands.add_workout(workout_id=4, workout_name="exercises_by_ivan_adamov", workout_frequency=1)

    await commands.add_program_workout(program_id=1, workout_id=1)
    await commands.add_program_workout(program_id=2, workout_id=2)
    await commands.add_program_workout(program_id=2, workout_id=3)
    await commands.add_program_workout(program_id=4, workout_id=4)

    for exercise_pw in exercises_paul_wade:
        await commands.add_exercise(
            exercise_id=exercise_pw.exercise_id,
            exercise_name=exercise_pw.exercise_name,
            exercise_duration=exercise_pw.exercise_duration,
            exercise_definition=exercise_pw.exercise_definition,
            exercise_file_type="animation",
            exercise_file=exercise_pw.exercise_file
        )
        await commands.add_workout_exercise(
            workout_id=2,
            exercise_id=exercise_pw.exercise_id,
            amount_of_sets=2,
            amount_of_repetitions=4
        )

    for child_m_w in child_morning_workout:
        await commands.add_exercise(
            exercise_id=child_m_w.exercise_id,
            exercise_name=child_m_w.exercise_name,
            exercise_duration=child_m_w.exercise_duration,
            exercise_definition=child_m_w.exercise_definition,
            exercise_file_type="animation",
            exercise_file=child_m_w.exercise_file
        )
        await commands.add_workout_exercise(
            workout_id=1,
            exercise_id=child_m_w.exercise_id,
            amount_of_sets=1,
            amount_of_repetitions=1
        )
    for exercise in exercises_by_ivan_adamov:
        last_exercise_id = await commands.last_exercise_id()
        if exercise.exercise_id is None:
            exercise_id = last_exercise_id + 1
        await commands.add_exercise(
            exercise_id=exercise_id,
            exercise_name=exercise.exercise_name,
            exercise_duration=exercise.exercise_duration,
            exercise_definition=exercise.exercise_definition,
            exercise_file_type="video",
            exercise_file=exercise.exercise_file
        )
        await commands.add_workout_exercise(
            workout_id=4,
            exercise_id=exercise_id,
            amount_of_sets=1,
            amount_of_repetitions=1
        )
    # await message.answer("БД оновлена")

    # workout_id = 1
    # workout_name = "Workout_one"
    #
    # await commands.add_workout_to_list(workout_id=workout_id, workout_name=workout_name
    #                                    # , user_id=user_id, level_complete=level_complete
    #                                    )
    # exercise_id = 1
    # exercise_name = "Присідання"
    # exercise_duration = 1
    # exercise_definition = "Хм... просто сука присядь!"
    # exercise_file = "AgACAgIAAxkBAAICcV6jF5kAARvDMn99PQuVe9fBg-TKcAACQ64xG0WQGEm4F3v9dsbAAg7Hwg8ABAEAAwIAA3kAA9c_BgABGQQ"
    # await commands.add_exercise_to_list(exercise_id=exercise_id, exercise_name=exercise_name,
    #                                     exercise_duration=exercise_duration,
    #                                     exercise_definition=exercise_definition, exercise_file=exercise_file)

    # exercise_id = 1
    # exercise_name = "Присідання"
    # exercise_approaches = 3
    # exercise_repetitions = 12
    # workout_table_name = 'Workout_one'
    # await commands.add_exercise_to_workout(workout_table_name=workout_table_name, exercise_id=exercise_id,
    #                                        exercise_name=exercise_name,
    #                                        exercise_approaches=exercise_approaches,
    #                                        exercise_repetitions=exercise_repetitions)
