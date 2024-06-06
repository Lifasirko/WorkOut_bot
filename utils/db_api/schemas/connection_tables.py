from datetime import datetime

from sqlalchemy import Column, BigInteger, Integer, ForeignKey, Boolean, DateTime, Time
from sqlalchemy.dialects.postgresql import TIMESTAMP

from utils.db_api.db_gino import db, TimedBaseModel, BaseModel


class User_program(TimedBaseModel):
    __tablename__ = 'user_program'
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'), primary_key=True)
    program_id = Column(Integer, ForeignKey('workouts.workout_id'), primary_key=True)


class Program_workout(TimedBaseModel):
    __tablename__ = 'program_workout'
    program_id = Column(Integer, ForeignKey('workouts.workout_id'), primary_key=True)
    workout_id = Column(Integer, ForeignKey('workouts.workout_id'), primary_key=True)
    workout_day = Column(Integer)


class Workout_exercise(TimedBaseModel):
    __tablename__ = 'workout_exercise'
    workout_id = Column(Integer, ForeignKey('workouts.workout_id'), primary_key=True)
    exercise_id = Column(Integer, ForeignKey('exercises.exercise_id'), primary_key=True)
    exercise_number = Column(Integer)
    amount_of_sets = Column(Integer)
    amount_of_repetitions = Column(Integer)
    time_dependant = Column(Boolean, default=False)


class Workout_schedule(TimedBaseModel):
    __tablename__ = 'workout_schedule'
    user_id = Column(BigInteger, primary_key=True)  # , ForeignKey('users.telegram_id')
    monday = Column(Time(), default=None)
    tuesday = Column(Time(), default=None)
    wednesday = Column(Time(), default=None)
    thursday = Column(Time(), default=None)
    friday = Column(Time(), default=None)
    saturday = Column(Time(), default=None)
    sunday = Column(Time(), default=None)
