import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove

from handlers.users.options import options_keyboard
from handlers.users.registration import share_number
from loader import dp
from utils.db_api import quick_commands as commands
from utils.notify_admins import added_new_user_notify


@dp.message_handler(CommandStart(deep_link=re.compile("^parent+[0-9]{9}$")))
async def send_ref_link_to_child(message: types.Message):
    name = message.from_user.full_name
    deep_link_args = message.get_args()
    referral = int(deep_link_args[-9:])
    await commands.add_user(telegram_id=message.from_user.id, name=name, referral=referral)
    await commands.make_child(telegram_id=message.from_user.id)
    await message.answer(
        "\n".join(
            [
                f'Вітаю, {name}!',
                f'Для початку тренувань необхідно зареєструватись.',
            ]))
    await added_new_user_notify(dp=dp, message=message, referral=referral, child=True)
    print("child")
    await share_number(message=message)


@dp.message_handler(CommandStart(deep_link=re.compile("^[0-9]{9}$")),
                    # IsPrivate() #block1 14.04.22.22:32
                    )
async def bot_start_deep_link(message: types.Message,
                              # state: FSMContext  # block1 14.04.22.22:32
                              ):
    name = message.from_user.full_name
    # print(message.get_args())
    deep_link_args = message.get_args()

    referral = int(deep_link_args)
    await commands.add_user(telegram_id=message.from_user.id, name=name, referral=referral)

    await message.answer(
        "\n".join(
            [
                f'Вітаю, {name}!',
                f'Для початку тренувань необхідно зареєструватись.',
            ]))
    await added_new_user_notify(dp=dp, message=message, referral=referral)
    await share_number(message=message)
    # await state.set_state("registration")


@dp.message_handler(state="blocked")
async def blocked_user(message: types.Message):
    await message.answer(text="Ви були заблоковані. Зверніться до керівника чи адміністратора.")


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    if await commands.select_user(telegram_id=message.from_user.id) is None:
        name = message.from_user.full_name
        # print(message.get_args())
        await commands.add_user(telegram_id=message.from_user.id, name=name)

        await message.answer(
            "\n".join(
                [
                    f'Вітаю, {name}!',
                    f'Для початку тренувань необхідно зареєструватись.',
                ]))
        await added_new_user_notify(dp=dp, message=message)
        await share_number(message=message)
    else:
        name = message.from_user.full_name
        phone_number = await commands.select_user_phone_n(telegram_id=message.from_user.id)
        await message.answer(f"{name}, Ви вже були зареєстровані у базі за номером телефону:\n"
                             f"{phone_number}\n",
                             reply_markup=ReplyKeyboardRemove())
        await options_keyboard(message=message)
