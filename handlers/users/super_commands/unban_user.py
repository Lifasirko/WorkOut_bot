from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import ADMINS
from loader import dp

async def get_blocked_users_kb_func():


@dp.message_handler(Command("unban"))
async def choose_blocked_users(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        markup = await get_blocked_users_kb_func()

        await message.answer("Обери користувача, якого розблокувати", reply_markup=markup)
    else:
        await message.answer("Ви не можете користуватись цією командою")






@dp.message_handler(state="get_text_for_message_to_users")
async def send_message_to_users(message: types.Message, state: FSMContext):
    users_list = await commands.get_users()
    state = dp.current_state(chat=chat_id, user=user_id)
    await state.set_state(User.accepted)
    await state.finish()
