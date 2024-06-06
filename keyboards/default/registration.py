from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

registrate = ReplyKeyboardMarkup(resize_keyboard=True,
                                 keyboard=[
                                     [
                                         KeyboardButton(text="Зареєструватись!",
                                                        request_contact=True)
                                     ]
                                 ])
