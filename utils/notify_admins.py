import logging

from aiogram import Dispatcher, types

from data.config import ADMINS
from utils.db_api import quick_commands as commands


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот Запущен и готов к работе")

        except Exception as err:
            logging.exception(err)


async def on_shutdown_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот погашен")

        except Exception as err:
            logging.exception(err)


async def added_new_user_notify(dp: Dispatcher, message: types.Message, referral: int = None, child: bool = None):
    for admin in ADMINS:
        try:
            count = await commands.count_users()
            if referral:
                if child is True:
                    await dp.bot.send_message(
                        admin,
                        f"Новий зареєстрований користувач ({message.from_user.full_name}) в базі!\n"
                        f"id користувача:\n"
                        f"{message.from_user.id}\n"
                        f"Його привів користувач:\n"
                        f"{referral}\n"
                        f"і це його дитина!!!"
                        f"У базі <b>{count}</b> користувачів\n"
                    )

                else:
                    await dp.bot.send_message(
                        admin,
                        f"Новий зареєстрований користувач ({message.from_user.full_name}) в базі!\n"
                        f"id користувача:\n"
                        f"{message.from_user.id}\n"
                        f"Його привів користувач:\n"
                        f"{referral}"
                        f"У базі <b>{count}</b> користувачів\n"
                    )
            else:
                await dp.bot.send_message(
                    admin,
                    f"Новий зареєстрований користувач ({message.from_user.full_name}) в базі!\n"
                    f"id користувача:\n"
                    f"{message.from_user.id}\n"
                    f"Прийшов сам\n"
                    f"У базі <b>{count}</b> користувачів\n"
                )

        except Exception as err:
            logging.exception(err)


async def registered_new_user_notify(dp: Dispatcher, message: types.Message, phone_n):
    for admin in ADMINS:
        try:
            count = await commands.count_users()
            await dp.bot.send_message(
                admin,
                f"Новий зареєстрований користувач ({message.from_user.full_name}) в базі!\n"
                f"id користувача:\n"
                f"{message.from_user.id}\n"
                f"Телефон користувача:\n"
                f"{phone_n}\n"
                f"У базі <b>{count}</b> користувачів\n"
            )

        except Exception as err:
            logging.exception(err)


async def try_register_not_employee_notify(dp: Dispatcher, message: types.Message, phone_n, text):
    for admin in ADMINS:
        try:
            # count = await commands.count_users()
            await dp.bot.send_message(admin,
                                      f"Пытается зарегистрироваться не сотрудник ({message.from_user.full_name})\n"
                                      f"Телефон пользователя:\n"
                                      f"{phone_n}\n"
                                      f"{text}")

        except Exception as err:
            logging.exception(err)


async def some_problem_notify(dp: Dispatcher, message: types.Message, problem_stage: str = None):
    for admin in ADMINS:
        try:
            # count = await commands.count_users()
            await dp.bot.send_message(admin,
                                      f"Виникла помилка на етапі:\n"
                                      f"{problem_stage}\n"
                                      f"у користувача:\n"
                                      f"{message.from_user.id}"
                                      )

        except Exception as err:
            logging.exception(err)
