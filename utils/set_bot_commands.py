from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустити бота"),
        types.BotCommand("help", "Отримати довідку"),
        types.BotCommand("options", "Опції"),
        types.BotCommand("plan_next_workout", "Запланувати наступне тренування"),
        types.BotCommand("get_ref_link", "Отримати лінк реферера"),
        types.BotCommand("reset_state", "Скинути стани користувача"),

        # types.BotCommand("test", "test"),

    ])
