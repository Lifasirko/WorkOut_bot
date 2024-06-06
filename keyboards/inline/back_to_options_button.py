from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import options_callback

back_to_options_button = InlineKeyboardMarkup(row_width=1)

go_to_options = InlineKeyboardButton(text="Повернутися до опцій", callback_data=options_callback.new(type="Callback"))
back_to_options_button.insert(go_to_options)


async def back_to_options_button_func(text: str = None):
    if text:
        inline_button = InlineKeyboardButton(text=text, callback_data=options_callback.new(type="Callback"))
    else:
        inline_button = InlineKeyboardButton(text="Повернутися до опцій",
                                             callback_data=options_callback.new(type="Callback"))
    return inline_button
