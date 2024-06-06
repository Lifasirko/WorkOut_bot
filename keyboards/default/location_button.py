from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                               keyboard=[
                                   [
                                       KeyboardButton(text="Надіслати місцеположення",
                                                      request_location=True, one_time_keyboard=True)
                                   ]
                               ])
