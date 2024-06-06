from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command("reset_state"), state="*")
async def reset_state(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Стан знятий")
