from sqlalchemy import Column, String, Integer, Boolean, BigInteger, ForeignKey

from utils.db_api.db_gino import BaseModel


class Programs(BaseModel):
    __tablename__ = 'programs'
    program_id = Column(Integer, primary_key=True)
    program_name = Column(String(100))
    program_is_free = Column(Boolean, default=False)
    # program_price = Column(Integer) # TODO: прописать везде установку цены. Не менее 1 доллара
    morning_program = Column(Boolean, default=False)
    level_program = Column(String(100), default=None)
    sex_program = Column(String(100), default=None)
    age_program = Column(String(100), default=None)
    random_workout = Column(Boolean, default=False)
    creator = Column(BigInteger, ForeignKey('users.telegram_id'))
