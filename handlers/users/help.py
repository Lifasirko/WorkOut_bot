from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.config import ADMINS
from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        text = [
            'Список команд: ',
            '/start - Почати діалог',
            '/help - Отримати довідку',
            '/get_ref_link - Отримати лінк реферера',
            '/update_db - Оновити БД',
            '/options - Перейти до опцій',
            '/plan_next_workout - Запланувати наступне тренування',
            '/test - Протестувати функцію',
            '/send_message - Надіслати повідомлення усім користувачам',
            '/send_message_to_admins - Надіслати повідомлення адміністраторам',
            '/backup - Зробити бекап бази'
        ]
        await message.answer('\n'.join(text))
    else:
        text = [
            'Список команд: ',
            '/start - Почати діалог',
            '/help - Отримати довідку',
            '/get_ref_link - Отримати лінк реферера',
            '/options - Перейти до опцій',
            '/plan_next_workout - Запланувати наступне тренування'
        ]
        await message.answer('\n'.join(text))
