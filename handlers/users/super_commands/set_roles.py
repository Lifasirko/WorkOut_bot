from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from loader import dp
from utils.misc import rate_limit


@dp.message_handler(Command("get_ref_link"))
async def set_admin(message: types.Message):
    bot_user = await dp.bot.get_me()

    # Формируем диплинк-ссылку
    ref_link = f"http://t.me/{bot_user.username}?start={message.from_user.id}"
    await message.answer(f'{ref_link}')