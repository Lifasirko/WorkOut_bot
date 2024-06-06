from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import ADMINS
from loader import dp
from utils.db_api import quick_commands as commands


@dp.message_handler(Command("send_message"))
async def get_text_for_message_to_users(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        await message.answer("Надішли текст повідомлення для усіх користувачів")
        await state.set_state("get_text_for_message_to_users")
    else:
        await message.answer("Ви не можете користуватись цією командою")


@dp.message_handler(state="get_text_for_message_to_users")
async def send_message_to_users(message: types.Message, state: FSMContext):
    text = message.text
    users_list = await commands.get_users()
    for telegram_id in users_list:
        await dp.bot.send_message(chat_id=telegram_id,
                                  text=text)
    await state.finish()


@dp.message_handler(Command("send_message_to_admins"))
async def get_text_for_message_to_users(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        await message.answer("Надішли текст повідомлення для адміністраторів")
        await state.set_state("get_text_for_message_to_admins")
    else:
        await message.answer("Ви не можете користуватись цією командою")


@dp.message_handler(state="get_text_for_message_to_admins")
async def send_get_text_for_message_to_admins(message: types.Message, state: FSMContext):
    text = message.text
    for admin in ADMINS:
        await dp.bot.send_message(chat_id=admin,
                                  text=text)
    await state.finish()
