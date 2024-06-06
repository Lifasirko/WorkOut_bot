from sqlalchemy import Column, BigInteger, String, sql, Integer, Boolean

from utils.db_api.db_gino import TimedBaseModel, BaseModel


class Workouts(BaseModel):
    __tablename__ = 'workouts'
    workout_id = Column(Integer, primary_key=True, autoincrement=True)
    workout_name = Column(String(100))
    workout_frequency = Column(Integer)

    # user_id = Column(BigInteger)
    # level_complete = Column(Boolean)

    # exercise_1 = Column(Integer)
    # exercise_1_approaches = Column(Integer)
    # exercise_1_repetitions = Column(Integer)
    #
    # exercise_2 = Column(Integer)
    # exercise_2_approaches = Column(Integer)
    # exercise_2_repetitions = Column(Integer)
    #
    # exercise_3 = Column(Integer)
    # exercise_3_approaches = Column(Integer)
    # exercise_3_repetitions = Column(Integer)
    #
    # exercise_4 = Column(Integer)
    # exercise_4_approaches = Column(Integer)
    # exercise_4_repetitions = Column(Integer)
    #
    # exercise_5 = Column(Integer)
    # exercise_5_approaches = Column(Integer)
    # exercise_5_repetitions = Column(Integer)
    #
    # exercise_6 = Column(Integer)
    # exercise_6_approaches = Column(Integer)
    # exercise_6_repetitions = Column(Integer)
    #
    # exercise_7 = Column(Integer)
    # exercise_7_approaches = Column(Integer)
    # exercise_7_repetitions = Column(Integer)
    #
    # exercise_8 = Column(Integer)
    # exercise_8_approaches = Column(Integer)
    # exercise_8_repetitions = Column(Integer)
    #
    # exercise_9 = Column(Integer)
    # exercise_9_approaches = Column(Integer)
    # exercise_9_repetitions = Column(Integer)
    #
    # exercise_10 = Column(Integer)
    # exercise_10_approaches = Column(Integer)
    # exercise_10_repetitions = Column(Integer)
    #
    # exercise_11 = Column(Integer)
    # exercise_11_approaches = Column(Integer)
    # exercise_11_repetitions = Column(Integer)





