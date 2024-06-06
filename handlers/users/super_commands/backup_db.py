from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import OWNERS
from loader import dp
from utils.db_api import quick_commands as commands


@dp.message_handler(Command("backup"))
async def backup_database(message: types.Message):
    programs = await commands.get_programs_id()
    workouts = await commands.get_workouts_id()
    exercises = await commands.get_exercises_id()
    # user_programs = await commands.get_user_programs() # TODO: Дописать бэкапы для всего
    # print(user_programs)
    backup_text = list()
    backup_text.append("await commands.add_user(telegram_id=1)")
    for owner in OWNERS:

        for program in programs:
            program_id = int(program.program_id)
            program_name = await commands.get_program_name(program_id)
            program_is_free = await commands.get_program_is_free(program_id)
            morning_program = await commands.get_morning_program(program_id)
            level_program = await commands.get_level_program(program_id)
            sex_program = await commands.get_sex_program(program_id)
            age_program = await commands.get_age_program(program_id)
            random_workout = await commands.get_random_workout(program_id)
            creator = await commands.get_creator(program_id)
            text = f"await commands.add_program(program_id={program_id}, program_name={program_name}, program_is_free={program_is_free}, morning_program={morning_program}, level_program={level_program}, sex_program={sex_program}, age_program={age_program}, random_workout={random_workout}, creator={creator})"
            backup_text.append(text)

        for workout in workouts:
            workout_id = int(workout.workout_id)
            workout_name = await commands.get_workout_name(workout_id)
            workout_frequency = await commands.get_workout_frequency(workout_id)
            text = f"await commands.add_workout(workout_id={workout_id}, workout_name={workout_name}, workout_frequency={workout_frequency})"
            backup_text.append(text)

        for exercise in exercises:
            exercise_id = exercise.exercise_id
            exercise_name = await commands.get_exercise_name(exercise_id)
            exercise_description = await commands.get_exercise_description(exercise_id)
            exercise_file_type = await commands.get_exercise_file_type(exercise_id)
            exercise_file = await commands.get_exercise_file(exercise_id)
            exercise_duration = await commands.get_exercise_duration(exercise_id)
            text = f"await commands.add_exercise(exercise_id={exercise_id}, exercise_name={exercise_name}, " \
                   f"exercise_duration={exercise_duration}, exercise_definition={exercise_description}, " \
                   f"exercise_file_type={exercise_file_type}, exercise_file={exercise_file})"
            backup_text.append(text)

        # for user_program in

        await dp.bot.send_message(chat_id=owner, text=backup_text)

        print(backup_text)
