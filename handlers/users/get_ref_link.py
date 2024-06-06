from typing import Union

from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline.back_to_options_button import back_to_options_button_func
from keyboards.inline.callback_datas import get_referral_link_callback, get_parent_link_callback
from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'get_ref_link')
@dp.message_handler(Command("get_ref_link"))
async def get_ref_link(message: Union[Message, CallbackQuery]):
    bot_user = await dp.bot.get_me()

    # Формируем диплинк-ссылку
    ref_link = f"http://t.me/{bot_user.username}?start={message.from_user.id}"
    if isinstance(message, Message):
        await message.answer(f'{ref_link}')
    if isinstance(message, CallbackQuery):
        await message.message.edit_reply_markup()
        await message.message.answer(f'{ref_link}')


@dp.callback_query_handler(get_referral_link_callback.filter())
async def get_ref_link_cb(message):
    await get_ref_link(message)


@rate_limit(5, 'get_parent_link')
@dp.message_handler(Command("get_parent_link"))
async def get_parent_link(message: Union[Message, CallbackQuery]):
    bot_user = await dp.bot.get_me()

    # Формируем диплинк-ссылку
    ref_link = f"http://t.me/{bot_user.username}?start=parent{message.from_user.id}"
    if isinstance(message, Message):
        await message.answer(f'{ref_link}')
    if isinstance(message, CallbackQuery):
        # await message.message.edit_reply_markup()
        markup = await back_to_options_button_func()
        await message.message.answer(f'{ref_link}', reply_markup=markup)


@dp.callback_query_handler(get_parent_link_callback.filter())
async def get_parent_link_cb(message):
    await get_parent_link(message)
