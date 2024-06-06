from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey

from utils.db_api.db_gino import BaseModel, TimedBaseModel


class Payments(TimedBaseModel):
    __tablename__ = 'payments'
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    payment_name = Column(String(100))
    payment_service = Column(String(100))
