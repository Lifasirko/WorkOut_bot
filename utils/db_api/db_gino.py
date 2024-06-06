from typing import List

from aiogram import Dispatcher
from gino import Gino
import sqlalchemy as sa
from sqlalchemy import Column, DateTime

from data import config

db = Gino()


# Пример из https://github.com/aiogram/bot/blob/master/app/models/db.py

class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=db.func.now())
    updated_at = Column(DateTime(True),
                        default=db.func.now(),
                        onupdate=db.func.now(),
                        server_default=db.func.now())


async def on_startup(dispatcher: Dispatcher):
    print("Установка связи с PostgreSQL")
    await db.set_bind(config.POSTGRES_URI)


# async def delete_table(table):
#     table = table
#     table.drop(engine)


# async def delete_table_users_most():
#     users_most = Users_most
#     users_most.drop(engine)
#     print("Удаляем таблицу Users_most")

    # from sqlalchemy import *
    # # imports all needed modules from sqlalchemy
    # engine = create_engine('postgresql://python:python@127.0.0.1/production')
    # # connection properties stored
    # metadata = MetaData()
    # # stores the 'production' database's metadata
    # users = Table('users',
    #               metadata,
    #               Column('user_id', Integer),
    #               Column('first_name', String(150)),
    #               Column('last_name', String(150)),
    #               Column('email', String(255)),
    #               schema='python')
    # # defines the 'users' table structure in the 'python' schema of our connection to the 'production' db
    # users.create(engine)
    # # creates the users table
    # users.drop(engine)
    # # drops the users table
