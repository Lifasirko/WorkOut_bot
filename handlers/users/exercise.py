from typing import Union

from aiogram.types import Message, CallbackQuery

from keyboards.inline.callback_datas import exercises_list_callback, start_exercise_callback
# from keyboards.inline.choose_workout_menu import choose_workout_menu
# from keyboards.inline.start_exercise_menu import workout_menu
from loader import dp
from utils.db_api import quick_commands as commands


@dp.callback_query_handler(exercises_list_callback.filter())
# state=Registration_states.Registered
async def exercises_list(message: Union[Message, CallbackQuery]):
    # await message.answer(cache_time=60)

    exercises_list_workout = (
        ('name', 2, 15),
        ('another', 3, 20),
    )
    text_add = '\n'.join(
        [
            f'{num}. {name}, {n_sets} {n_reps}..'
            for num, (name, n_sets, n_reps) in enumerate(exercises_list_workout, start=1)
        ]
    )

    await message.answer(text=text_add,
                         # reply_markup=workout_menu
                         )


@dp.callback_query_handler(start_exercise_callback.filter())
async def start_exercises(call: CallbackQuery):
    await call.answer(cache_time=60)
    exercise_id = 1
    exercise_file = await commands.get_exercise_file(exercise_id=exercise_id)
    text = await commands.get_exercise_definition(exercise_id=exercise_id)
    # await call.message.reply_video(video=exercise_file, caption=text,reply_markup=)

    # workout_id = Workout_one()
    # exercise_duration = await commands.get_exercise_duration(exercise_id=1)
    # exercise_approaches = await commands.get_exercise_approaches(workout_id=workout_id, exercise_id=1)
    # exercise_repetitions = await commands.get_exercise_repetitions(workout_id=workout_id, exercise_id=1)
    # exercise_approaches_now = 0
    # exercise_repetitions_now = 0
    # while exercise_approaches_now < exercise_approaches:
    #     exercise_approaches += 1

# @dp.callback_query_handler(next_exercises_callback.filter())
#         while exercise_repetitions_now < exercise_repetitions:
