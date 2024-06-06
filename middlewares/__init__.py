from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .scheduler import SchedulerMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    # dp.middleware.setup(SchedulerMiddleware())
