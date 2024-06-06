from sqlalchemy import Column, String, Integer

from utils.db_api.db_gino import BaseModel


class Exercises(BaseModel):
    __tablename__ = 'exercises'
    exercise_id = Column(Integer, primary_key=True, autoincrement=True)
    exercise_name = Column(String(100))
    exercise_duration = Column(Integer)
    exercise_definition = Column(String(100000))
    exercise_file_type = Column(String(100))
    exercise_file = Column(String(1000))
