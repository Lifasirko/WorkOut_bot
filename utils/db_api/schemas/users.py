from sqlalchemy import Column, BigInteger, String, sql, Boolean, Date, DateTime, Integer

from utils.db_api.db_gino import TimedBaseModel


class Users(TimedBaseModel):
    __tablename__ = 'users'
    telegram_id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    phone_number = Column(String(100), unique=True)
    # program_id = Column(Integer)
    real_name = Column(String(100))
    referral = Column(BigInteger)
    payment = Column(Boolean)
    role = Column(String(100))
    birthday = Column(Date())
    sex = Column(String(100))
    level = Column(String(100))
    next_workout_reminder = Column(DateTime())
    scheduled_reminder = Column(Boolean)
    timezone_info = Column(String)
    is_child = Column(Boolean, default=None)

    query: sql.Select
