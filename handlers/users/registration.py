from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from handlers.users.options import options_keyboard
from keyboards.default import registration
from loader import dp
from utils import registered_new_user_notify, try_register_not_employee_notify
from utils.db_api import quick_commands as commands
from utils.db_api.schemas.users import Users
from utils.notify_admins import some_problem_notify


@dp.message_handler(Command("reg"), state="registration")
async def share_number(message: types.Message,
                       # state: FSMContext#block1 14.04.22.22:32
                       ):
    await message.answer("Для реєстрації натисніть кнопку знизу", reply_markup=registration.registrate)
    # await Registration_states.Not_registered.set()#block1 14.04.22.22:32


@dp.message_handler(content_types=types.ContentType.CONTACT,
                    # state="registration"  # block1 14.04.22.22:32
                    )
async def get_contact(message: types.Message, state: FSMContext):
    await state.finish()
    contact = message.contact
    phone_n = message.contact.phone_number
    phone_n = "+38" + phone_n[-10:]  # Берем телефон по формату +38ХХХХХХХХХХ
    check_phone_n_users = await Users.query.where(Users.phone_number == phone_n).gino.first()
    # Проверяем, есть ли пользователь с присланным номером телефона в БД Users
    user_id = await commands.select_user_by_phone_number(phone_number=phone_n)
    name_r = await commands.get_user_real_name(telegram_id=message.from_user.id)
    if name_r is None:
        name = message.from_user.username
    else:
        name = name_r
    real_name = message.contact.full_name
    if check_phone_n_users is None:
        await message.answer(f"{name}, Вас було зареєстровано у базі за номером телефону:\n"
                             f"{contact.phone_number}\n"
                             f"Дякуємо!\n",
                             reply_markup=ReplyKeyboardRemove())
        await registered_new_user_notify(dp=dp, message=message, phone_n=phone_n)
        await options_keyboard(message=message)
        await commands.update_user_phone_n(telegram_id=message.from_user.id, phone_number=phone_n)
        await commands.update_user_real_name(telegram_id=message.from_user.id, real_name=real_name)

    elif check_phone_n_users is not None and user_id is None:
        await message.answer(f"{name}, Вас було зареєстровано у базі за номером телефону:\n"
                             f"{contact.phone_number}\n"
                             f"Дякуємо!\n",
                             reply_markup=ReplyKeyboardRemove())
        await options_keyboard(message=message)

    elif check_phone_n_users is not None:
        if message.from_user.id == user_id:
            await message.answer(f"{name}, Ви вже були зареєстровані у базі за номером телефону:\n"
                                 f"{contact.phone_number}\n",
                                 reply_markup=ReplyKeyboardRemove())
            await options_keyboard(message=message)
        else:
            text = "Цей номер телефону вже зареєстрований. Зверніться до адміністратора."
            await message.answer(text=text,
                                 reply_markup=ReplyKeyboardRemove())
            await try_register_not_employee_notify(dp=dp, message=message, phone_n=phone_n, text=text)
            await state.set_state("blocked")
    else:
        await message.answer("Виникла помилка! Зверніться до керівника чи адміністратора.")
        await some_problem_notify(dp=dp, message=message, problem_stage="get_contact")
    #     await state.set_state("blocked")
