from data import config
from handlers.users.reminder import notify_user, notify_user_schedule
from handlers.users.update_db import update_db
from keyboards.inline.choose_frequency_and_time import make_schedule_dialog
from loader import db, bot, scheduler, registry
# from utils import on_startup_notify
from utils.db_api import db_gino
from utils.set_bot_commands import set_default_commands


def set_scheduler_jobs(scheduler, bot, config):
    # scheduler.add_job(notify_user, "interval", seconds=5, args=(131445541,))
    scheduler.add_job(notify_user, "interval", minutes=1)
    scheduler.add_job(notify_user_schedule, "interval", minutes=1)


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    print("Подключаем БД")
    await db_gino.on_startup(dp)
    print("Готово")

    print("Чистим базу")
    # await db.gino.drop_all()
    # await delete_table_users_most() # TODO: разобраться как удалять одну таблицу (DROP TABLE {table name} — таблиця)
    # await db.gino.drop.table('Workout_exercise')
    print("Готово")

    print("Создаем таблицы")
    await db.gino.create_all()
    print("Готово")

    print("Обновляем БД")
    await update_db()
    print("Готово")

    print("Запускаем запуск по расписанию")
    set_scheduler_jobs(scheduler, bot, config)
    scheduler.start()
    print("Готово")

    print("Запускаем виджеты")
    # registry = DialogRegistry(dp)
    registry.register(make_schedule_dialog)
    print("Готово")

    await on_startup_notify(dp)
    await set_default_commands(dp)


async def on_shutdown(dp):
    from utils.notify_admins import on_shutdown_notify
    await on_shutdown_notify(dp)
    await bot.close()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True, on_shutdown=on_shutdown)

    # TODO: 1. Закончить все TODO!
    # TODO: 1.1. проверить виснет ли бот на цикле синхронной функции у других юзеров
    # TODO: 1.2. функция создания своей тренировки (название, перечень упражнений, повторы, подходы, длительность)
    # TODO: 1.3. дописать бэкапы

    # TODO: 2. повесить на все ремайндеры клавиатуру с началом тренировки + продолжение тренировки с главного меню
    # TODO: 3. прописать все записи в history
    # TODO: 4. при напоминании - кнопка начала тренировки(выбирать следующую, за последней законченной)
    # TODO: 5. Взять все требуемые материалы
    # TODO: 6. выгрузить на сервер

    # TODO: 5.1. видео для детской утренней зарядки
    # TODO: 5.2. взрослая утренняя зарядка

    # ________________________________________________ БЕТА ТЕСТ!!!________________________________________________#
    # TODO: 12. Добавить к мультивыбору кнопки удалить все напоминания и текст с выбранными днями и временем
    # TODO: 13. Фильтр по програмам в зависимости от возраста и тд
    # TODO: 14. функция таймера

    # ________________________________________________ интересности________________________________________________#
    # await call.message.answer("Дані оновлені. Запис в БД: \n" +
    #                           hcode(f"ваша стать - {user.sex}\n"), reply_markup=back_to_options_button
    #                           )  # TODO: так делается выделение текста
