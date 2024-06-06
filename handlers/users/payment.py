from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import Command

from data.program_pay import Weekly_access
from keyboards.inline.back_to_options_button import back_to_options_button_func, back_to_options_button
from keyboards.inline.callback_datas import payment_callback
from utils.db_api import quick_commands as commands

"""
Доп информация:

https://core.telegram.org/bots/api#sendinvoice
https://surik00.gitbooks.io/aiogram-lessons/content/chapter4.html
"""


@dp.callback_query_handler(payment_callback.filter())
async def show_invoices(message: types.Message):
    await bot.send_invoice(chat_id=message.from_user.id,
                           **Weekly_access.generate_invoice(),
                           payload="123456")


# @dp.shipping_query_handler()
# async def choose_shipping(query: types.ShippingQuery):
#     if query.shipping_address.country_code == "UA":
#         await bot.answer_shipping_query(shipping_query_id=query.id,
#                                         shipping_options=[POST_FAST_SHIPPING, POST_REGULAR_SHIPPING, PICKUP_SHIPPING],
#                                         ok=True)
#     elif query.shipping_address.country_code == "US":
#         await bot.answer_shipping_query(shipping_query_id=query.id,
#                                         ok=False,
#                                         error_message="Сюда не доставляем")
#     else:
#         await bot.answer_shipping_query(shipping_query_id=query.id,
#                                         shipping_options=[POST_REGULAR_SHIPPING],
#                                         ok=True)


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    markup = await back_to_options_button_func()
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Дякуємо за купівлю! Доступ буде надано протягом 10 хвилин.",
                           reply_markup=back_to_options_button)
    await commands.add_payment(user_id=pre_checkout_query.from_user.id)
    await commands.update_user_payment(telegram_id=pre_checkout_query.from_user.id)
