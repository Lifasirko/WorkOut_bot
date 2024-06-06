from aiogram.types import CallbackQuery

from keyboards.inline.back_to_options_button import back_to_options_button
from keyboards.inline.callback_datas import get_description_callback
from loader import dp


@dp.callback_query_handler(get_description_callback.filter())
async def get_description(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer(
        text=f"Цей бот написаний задля допомоги у підтримуванні вас у здоровому бла-бла-бла...\n",
        reply_markup=back_to_options_button
    )
