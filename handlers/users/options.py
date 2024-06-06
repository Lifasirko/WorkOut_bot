from typing import Union

# from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline.callback_datas import options_callback, additional_options_callback
from keyboards.inline.options_menu import additional_options_menu_func, options_menu_func
from loader import dp


# Та самая функция, которая отдает категории. Она может принимать как CallbackQuery, так и Message.
# Помимо этого, мы в нее можем отправить и другие параметры - category, subcategory, item_id,
# Поэтому ловим все остальное в **kwargs
@dp.callback_query_handler(options_callback.filter())
# state=Registration_states.Registered
async def options_keyboard(message: Union[Message, CallbackQuery]):
    markup = await options_menu_func(user_id=message.from_user.id)
    if isinstance(message, Message):
        await message.answer(text=f"Вітаю \n"
                                  f"Оберіть опцію, що вас цікавить\n",
                             reply_markup=markup)
    elif isinstance(message, CallbackQuery):
        await message.message.edit_reply_markup()
        await message.message.answer(text=f"Вітаю \n"
                                          f"Оберіть опцію, що вас цікавить\n",
                                     reply_markup=markup)


@dp.message_handler(Command("options"))
async def command_option_keyboard(message: Message):
    await options_keyboard(message=message)


@dp.callback_query_handler(additional_options_callback.filter())
# state=Registration_states.Registered
async def additional_options_keyboard(message: Union[Message, CallbackQuery], callback_data: dict = None):
    if isinstance(message, Message):
        updating_user_id = int(callback_data.get('updating_user_id'))
        markup = await additional_options_menu_func(user_id=message.from_user.id, updating_user_id=updating_user_id)
        await message.answer(text=f"Оберіть опцію, що вас цікавить\n",
                             reply_markup=markup)
    elif isinstance(message, CallbackQuery):
        markup = await additional_options_menu_func(user_id=message.from_user.id)
        await message.message.edit_reply_markup()
        await message.message.answer(text=f"Оберіть опцію, що вас цікавить\n",
                                     reply_markup=markup)


@dp.message_handler(Command("additional_options"))
async def command_additional_options(message: Message):
    await additional_options_keyboard(message=message)
