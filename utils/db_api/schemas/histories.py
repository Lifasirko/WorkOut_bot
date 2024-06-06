from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, BigInteger

from utils.db_api.db_gino import BaseModel, TimedBaseModel


class Program_history(TimedBaseModel):
    __tablename__ = 'program_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    program_id = Column(Integer, ForeignKey('workouts.workout_id'))
    program_is_done = Column(Boolean)


class Workout_history(TimedBaseModel):
    __tablename__ = 'workout_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    program_id = Column(Integer, ForeignKey('programs.program_id'))
    workout_id = Column(Integer, ForeignKey('workouts.workout_id'))
    workout_is_done = Column(Boolean, default=False)


class Exercises_history(TimedBaseModel):
    __tablename__ = 'exercises_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    exercise_id = Column(Integer, ForeignKey('workouts.workout_id'))
    workout_history_id = Column(Integer, ForeignKey('workout_history.id'))
    exercise_is_done = Column(Boolean)


class Changing_history(TimedBaseModel):
    __tablename__ = 'changes_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    program_id = Column(Integer, ForeignKey('programs.program_id'))
    program_id_changes_type = Column(String(100))
    program_id_changes_old = Column(String(100000))
    program_id_changes_new = Column(String(100000))
    workout_id = Column(Integer, ForeignKey('workouts.workout_id'))
    workout_id_changes_type = Column(String(100))
    workout_id_changes_old = Column(String(100000))
    workout_id_changes_new = Column(String(100000))
    exercise_id = Column(Integer, ForeignKey('workouts.workout_id'))
    exercise_id_changes_type = Column(String(100))
    exercise_id_changes_old = Column(String(100000))
    exercise_id_changes_new = Column(String(100000))
