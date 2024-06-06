from datetime import date

from asyncpg import UniqueViolationError
from sqlalchemy import and_, select, func, update

from data.config import conn
from utils.db_api.schemas.connection_tables import *
from utils.db_api.schemas.exercises import Exercises
from utils.db_api.schemas.histories import *
from utils.db_api.schemas.payments import Payments
from utils.db_api.schemas.programs import Programs
from utils.db_api.schemas.users import Users
from utils.db_api.schemas.workouts import Workouts


# _____________________________________________ Робота з таблицею Users _____________________________________________ #


async def add_user(telegram_id: int, name: str = None, phone_number: str = None, real_name: str = None,
                   referral: str = None, payment: bool = False, role: str = None, birthday: date = None,
                   sex: str = None, next_workout_reminder: datetime = None):
    try:
        user = Users(telegram_id=telegram_id, name=name, phone_number=phone_number, real_name=real_name,
                     referral=referral, payment=payment, role=role, birthday=birthday, sex=sex,
                     next_workout_reminder=next_workout_reminder)
        await user.create()
        free_programs = await get_free_programs()
        for program in free_programs:
            program_id = program.program_id
            await add_user_program(user_id=telegram_id, program_id=program_id)

    except UniqueViolationError:
        pass


async def select_all_users():
    users = await Users.query.gino.all()
    return users


async def select_user(telegram_id):
    user = await Users.query.where(Users.telegram_id == telegram_id).gino.first()
    return user


async def count_users():
    total = await db.func.count(Users.telegram_id).gino.scalar()
    conn.execute(total).fetchall()
    return total


async def select_user_phone_n(telegram_id):
    user = await Users.get(telegram_id)  # Работает только для первичных ключей
    user_phone_n = user.phone_number
    return user_phone_n


async def update_user_phone_n(telegram_id, phone_number):  # Записываем номер телефона в таблицу User
    user = await Users.get(telegram_id)
    await user.update(phone_number=phone_number).apply()


async def update_user_payment(telegram_id):  # Записываем номер телефона в таблицу User
    user = await Users.get(telegram_id)
    await user.update(payment=True).apply()


# async def select_user_name_r(telegram_id):
#     user = await Users.get(telegram_id)  # Работает только для первичных ключей
#     user_real_name = user.real_name
#     return user_real_name
#
#
# async def update_user_real_name(telegram_id, real_name):
#     user = await Users.get(telegram_id)
#     await user.update(real_name=real_name).apply()


async def select_user_by_phone_number(phone_number):
    user_telegram_id = Users.select('telegram_id').where(Users.phone_number == phone_number)
    return user_telegram_id


async def add_next_workout_reminder(telegram_id,
                                    next_workout_reminder):
    user = await Users.get(telegram_id)
    await user.update(next_workout_reminder=next_workout_reminder).apply()


async def get_next_workout_reminders():
    user = select([Users.telegram_id, Users.next_workout_reminder, Users.timezone_info])
    u2 = conn.execute(user)
    return u2


async def update_timezone(telegram_id, timezone):
    user = await Users.get(telegram_id)
    await user.update(timezone_info=timezone).apply()


async def get_timezone(telegram_id):
    user = await Users.get(telegram_id)  # Работает только для первичных ключей
    user_timezone = user.timezone_info
    return user_timezone


async def update_user_real_name(telegram_id, real_name):
    user = await Users.get(telegram_id)
    await user.update(real_name=real_name).apply()


async def get_user_real_name(telegram_id):
    user = await Users.get(telegram_id)  # Работает только для первичных ключей
    user_real_name = user.real_name
    return user_real_name


async def update_birthday(telegram_id, birthday):
    user = await Users.get(telegram_id)
    await user.update(birthday=birthday).apply()


async def get_birthday(telegram_id):
    user = await Users.get(telegram_id)  # Работает только для первичных ключей
    user_birthday = user.birthday
    return user_birthday


async def update_sex(telegram_id, sex):
    user = await Users.get(telegram_id)
    await user.update(sex=sex).apply()


async def get_sex(telegram_id):
    user = await Users.get(telegram_id)  # Работает только для первичных ключей
    user_sex = user.sex
    return user_sex


async def update_level(telegram_id, level):
    user = await Users.get(telegram_id)
    await user.update(level=level).apply()


async def get_level(telegram_id):
    user = await Users.get(telegram_id)  # Работает только для первичных ключей
    user_level = user.level
    return user_level


async def update_scheduled_reminder(telegram_id):
    user = await Users.get(telegram_id)
    await user.update(scheduled_reminder=True).apply()


async def get_scheduled_reminders():
    user = select([Users.telegram_id, Users.scheduled_reminder, Users.timezone_info])
    sr = conn.execute(user)
    return sr


async def get_users():
    user = select([Users.telegram_id])
    u2 = conn.execute(user)
    return u2


async def get_user_children(referral_id):
    children = select([Users.telegram_id, Users.name, Users.real_name]).where(
        and_(Users.referral == referral_id, Users.is_child == 'true'))
    children2 = conn.execute(children).fetchall()
    return children2


async def make_child(telegram_id):
    user = await Users.get(telegram_id)
    await user.update(is_child=True).apply()


# ___________________________________________ Робота з таблицею Programs ___________________________________________ #

async def add_program(program_id: int, program_name: str, program_is_free: bool = None, morning_program: bool = None,
                      level_program: str = None, sex_program: str = None, age_program: str = None,
                      random_workout: bool = None, creator: int = None):
    try:
        if creator is None:
            creator = 1
        program = Programs(program_id=program_id, program_name=program_name, program_is_free=program_is_free,
                           morning_program=morning_program, level_program=level_program, sex_program=sex_program,
                           age_program=age_program, random_workout=random_workout, creator=creator)
        await program.create()
    except UniqueViolationError:
        pass


async def get_programs_id():
    programs = select([Programs.program_id])
    u2 = conn.execute(programs).fetchall()
    return u2


async def create_new_program(program_id):
    try:
        new_program = Programs(program_id=program_id)
        await new_program.create()
        result = "success"
    except UniqueViolationError:
        result = "fail"
    return result


async def set_program_creator(program_id, user_id):
    program = await Programs.get(program_id)
    await program.update(creator=user_id).apply()


async def set_program_name(program_id, program_name):
    program = await Programs.get(program_id)
    await program.update(program_name=program_name).apply()


async def set_program_access(program_id, access):
    program = await Programs.get(program_id)
    if access == "True":
        access = True
    else:
        access = False
    await program.update(program_is_free=access).apply()


async def set_program_morning(program_id, morning):
    program = await Programs.get(program_id)
    if morning == "True":
        morning = True
    else:
        morning = False
    await program.update(morning_program=morning).apply()


async def set_program_level(program_id, level):
    program = await Programs.get(program_id)
    await program.update(level_program=level).apply()


async def set_program_sex(program_id, sex):
    program = await Programs.get(program_id)
    await program.update(sex_program=sex).apply()


async def set_program_age(program_id, age):
    program = await Programs.get(program_id)
    await program.update(age_program=age).apply()


async def get_free_programs():
    free_programs = select([Programs.program_id]).where(Programs.program_is_free == 'true')
    fp = conn.execute(free_programs).fetchall()
    print(fp)
    return fp


async def get_program_name(program_id):
    program = await Programs.get(program_id)
    program_name = program.program_name
    return program_name


async def get_program_is_free(program_id):
    program = await Programs.get(program_id)
    program_is_free = program.program_is_free
    return program_is_free


async def get_morning_program(program_id):
    program = await Programs.get(program_id)
    morning_program = program.morning_program
    return morning_program


async def get_level_program(program_id):
    program = await Programs.get(program_id)
    level_program = program.level_program
    return level_program


async def get_sex_program(program_id):
    program = await Programs.get(program_id)
    sex_program = program.sex_program
    return sex_program


async def get_age_program(program_id):
    program = await Programs.get(program_id)
    age_program = program.age_program
    return age_program


async def get_random_workout(program_id):
    program = await Programs.get(program_id)
    random_workout = program.random_workout
    return random_workout


async def get_creator(program_id):
    program = await Programs.get(program_id)
    creator = program.creator
    return creator


async def get_program_creator(program_id):
    program = await Programs.get(program_id)
    creator = program.creator
    return creator


async def get_last_program_id():
    program_id_last = select([Programs.program_id]).order_by(Programs.program_id.desc())
    program_id = conn.scalar(program_id_last)
    return program_id


# async def get_available_programs(user_id):
#     user = await Users.get(user_id)
#     available_programs =


# ___________________________________________ Робота з таблицею Workouts ___________________________________________ #

async def add_workout(workout_id: int, workout_name: str, workout_frequency: int = None):
    try:
        workout = Workouts(workout_id=workout_id, workout_name=workout_name, workout_frequency=workout_frequency)
        await workout.create()
    except UniqueViolationError:
        pass


async def get_workouts_id():
    workouts = select([Workouts.workout_id])
    u2 = conn.execute(workouts).fetchall()
    return u2


async def get_last_workout_id():
    last_workout_id = select([Workouts.workout_id]).order_by(Workouts.workout_id.desc())
    workout_id = conn.scalar(last_workout_id)
    return workout_id


async def create_new_workout(workout_id):
    try:
        workout = Workouts(workout_id=workout_id)
        await workout.create()
        result = "success"
    except UniqueViolationError:
        result = "fail"
    return result


async def set_workout_name(workout_id, workout_name):
    workout = await Workouts.get(workout_id)
    await workout.update(workout_name=workout_name).apply()


async def get_workout_name(workout_id):
    workout = await Workouts.get(workout_id)
    workout_name = workout.workout_name
    return workout_name


async def get_workout_frequency(workout_id):
    workout = await Workouts.get(workout_id)
    workout_frequency = workout.workout_frequency
    return workout_frequency


# ___________________________________________ Робота з таблицею Exercises ___________________________________________ #

async def add_exercise(exercise_id: int, exercise_name: str, exercise_duration: int = 1,
                       exercise_definition: str = None, exercise_file_type: str = None, exercise_file: str = None):
    try:
        exercise_id_one = select([Exercises.exercise_id]).order_by(Exercises.exercise_id.desc())
        highest_ex_id = conn.scalar(exercise_id_one)
        if exercise_id:
            exercise_id = exercise_id
        else:
            if highest_ex_id:
                exercise_id = highest_ex_id + 1
            else:
                exercise_id = 1
        exercise = Exercises(exercise_id=exercise_id, exercise_name=exercise_name, exercise_duration=exercise_duration,
                             exercise_definition=exercise_definition, exercise_file_type=exercise_file_type,
                             exercise_file=exercise_file)
        await exercise.create()
    except UniqueViolationError:
        pass


async def last_exercise_id():
    exercise_id_one = select([Exercises.exercise_id]).order_by(Exercises.exercise_id.desc())
    highest_ex_id = conn.scalar(exercise_id_one)
    return highest_ex_id


async def get_exercises_id():
    exercises = select([Exercises.exercise_id])
    u2 = conn.execute(exercises).fetchall()
    return u2


async def get_last_exercise_id():
    last_exercise_id = select([Exercises.exercise_id]).order_by(Exercises.exercise_id.desc())
    exercise_id = conn.scalar(last_exercise_id)
    return exercise_id


async def create_new_exercise(exercise_id):
    try:
        exercise = Exercises(exercise_id=exercise_id)
        await exercise.create()
        result = "success"
    except UniqueViolationError:
        result = "fail"
    return result


async def set_exercise_name(exercise_id, exercise_name):
    exercise = await Exercises.get(exercise_id)
    await exercise.update(exercise_name=exercise_name).apply()


async def set_exercise_duration(exercise_id, exercise_duration):
    exercise = await Exercises.get(exercise_id)
    exercise_duration = int(exercise_duration)
    await exercise.update(exercise_duration=exercise_duration).apply()


async def set_exercise_definition(exercise_id, exercise_definition):
    exercise = await Exercises.get(exercise_id)
    await exercise.update(exercise_definition=exercise_definition).apply()


async def set_exercise_file(exercise_id, exercise_file, exercise_file_type):
    exercise = await Exercises.get(exercise_id)
    await exercise.update(exercise_file=exercise_file).apply()
    await exercise.update(exercise_file_type=exercise_file_type).apply()


async def get_exercise_name(exercise_id):  # Запрос из sqlalchemy
    exercise_name = select([Exercises.exercise_name]).where(Exercises.exercise_id == exercise_id)
    en2 = conn.scalar(exercise_name)
    # exercise = await Exercises.get(exercise_id)
    # exercise_name = exercise.exercise_name
    return en2


async def get_exercise_description(exercise_id):
    exercise = select([Exercises.exercise_definition]).where(Exercises.exercise_id == exercise_id)
    exercise_description = conn.scalar(exercise)
    return exercise_description


async def get_exercise_file_type(exercise_id):
    exercise = select([Exercises.exercise_file_type]).where(Exercises.exercise_id == exercise_id)
    exercise_file_type = conn.scalar(exercise)
    return exercise_file_type


async def get_exercise_file(exercise_id):  # Запрос из sqlalchemy
    exercise = select([Exercises.exercise_file]).where(Exercises.exercise_id == exercise_id)
    exercise_file = conn.scalar(exercise)
    return exercise_file


async def get_exercise_duration(exercise_id):
    exercise = select([Exercises.exercise_duration]).where(Exercises.exercise_id == exercise_id)
    exercise_duration = conn.scalar(exercise)
    return exercise_duration


# ________________________________________ Робота з таблицями Users_Programs ________________________________________ #

async def add_user_program(user_id, program_id):
    try:
        user_prog = User_program(user_id=user_id, program_id=program_id)
        await user_prog.create()
    except UniqueViolationError:
        pass


async def get_user_programs():
    User_programs = select([User_program.user_id])
    u2 = conn.execute(User_program).fetchall()
    return u2


async def get_available_programs(user_id):
    available_programs = select([User_program.program_id]).where(User_program.user_id == user_id)
    ap = conn.execute(available_programs).fetchall()
    return ap


# _______________________________________ Робота з таблицями Programs_Workouts _______________________________________ #

async def add_program_workout(program_id, workout_id):
    try:

        prog_wo = Program_workout(program_id=program_id, workout_id=workout_id)
        await prog_wo.create()
    except UniqueViolationError:
        pass


async def get_workouts_in_program(program_id):  # Запрос из sqlalchemy
    workouts = select([Program_workout]).where(Program_workout.program_id == program_id)
    w2 = conn.execute(workouts).fetchall()
    # workouts = await Program_workout.query.where(Program_workout.program_id == program_id).gino.all()
    return w2


async def count_workouts_in_program(program_id):
    conditions = [Program_workout.program_id == program_id]
    total = await db.select([db.func.count()]).where(and_(*conditions)).gino.scalar()
    return total


# ______________________________________ Робота з таблицями Workouts_Exercises ______________________________________ #

async def add_workout_exercise(workout_id, exercise_id, amount_of_sets, amount_of_repetitions):
    try:
        wo_exercise = Workout_exercise(workout_id=workout_id, exercise_id=exercise_id,
                                       amount_of_sets=amount_of_sets,
                                       amount_of_repetitions=amount_of_repetitions)
        await wo_exercise.create()
    except UniqueViolationError:
        pass


async def get_exercises_in_workout(workout_id):  # Запрос из sqlalchemy
    exercises = select([Workout_exercise]).where(Workout_exercise.workout_id == workout_id)
    e2 = conn.execute(exercises).fetchall()
    return e2


async def count_exercises_in_workout(workout_id):
    total = select([func.count(Workout_exercise.workout_id)]).where(Workout_exercise.workout_id == workout_id)
    t2 = conn.scalar(total)
    return t2


async def get_exercise_sets(workout_id, exercise_id):
    exercise_sets = select([Workout_exercise.amount_of_sets]).where(
        and_(Workout_exercise.workout_id == workout_id, Workout_exercise.exercise_id == exercise_id))
    es2 = conn.scalar(exercise_sets)
    return es2


async def get_exercise_repetitions(workout_id, exercise_id):
    exercise_repetitions = select([Workout_exercise]).where(
        and_(Workout_exercise.workout_id == workout_id, Workout_exercise.exercise_id == exercise_id))
    er2 = conn.scalar(exercise_repetitions)
    return er2


async def is_time_dependant(workout_id, exercise_id):
    time_dependant = select([Workout_exercise.time_dependant]).where(
        and_(Workout_exercise.workout_id == workout_id, Workout_exercise.exercise_id == exercise_id))
    t_d = conn.scalar(time_dependant)
    return t_d


# _______________________________________ Робота з таблицями Workouts_history _______________________________________ #

async def add_workout_history(user_id, program_id, workout_id):
    exercise = Workout_history(user_id=user_id, program_id=program_id, workout_id=workout_id)
    await exercise.create()


async def make_workout_done(user_id, workout_id):
    wo = select([Workout_history.created_at]).where(
        and_(Workout_history.user_id == user_id, Workout_history.workout_is_done == 'false')
    ).order_by(Workout_history.updated_at.desc())
    last_workout = conn.scalar(wo)
    workout = update(Workout_history).where(
        and_(Workout_history.user_id == user_id, Workout_history.workout_id == workout_id,
             Workout_history.created_at == last_workout)).values(workout_is_done=True)
    conn.execute(workout)


async def get_last_workout(user_id):
    workout = select([Workout_history.program_id, Workout_history.workout_id]).where(
        and_(Workout_history.user_id == user_id, Workout_history.workout_is_done == 'true')
    ).order_by(Workout_history.updated_at.desc())
    last_workout = conn.execute(workout).first()
    print(last_workout)
    return last_workout


# _______________________________________ Робота з таблицями Exercises_history _______________________________________ #

async def add_exercise_history(user_id, workout_id, exercise_id):
    exercise = Exercises_history(user_id=user_id, workout_id=workout_id, exercise_id=exercise_id)
    await exercise.create()


async def make_exercise_done(user_id, workout_id, exercise_id):
    exercise = await Exercises_history.select('id').where(
        and_(user_id == user_id, workout_id == workout_id, exercise_id == exercise_id)).gino.scalar()
    await exercise.update(exercise_is_done=True).apply()


# ___________________________________________ Робота з таблицями Payments ___________________________________________ #


async def add_payment(user_id: int, payment_name: str = None, payment_service: str = None):
    try:
        payment_id_one = select([Payments.payment_id]).order_by(Payments.payment_id.desc())
        po = conn.scalar(payment_id_one)
        if po:
            payment_id = po + 1
        else:
            payment_id = 1
        payment = Payments(user_id=user_id, payment_id=payment_id, payment_name=payment_name,
                           payment_service=payment_service)
        await payment.create()
    except UniqueViolationError:
        pass


# _______________________________________ Робота з таблицями Workout_schedule _______________________________________ #


async def add_workout_schedule(user_id: int, monday: datetime.time = None, tuesday: datetime.time = None,
                               wednesday: datetime.time = None, thursday: datetime.time = None,
                               friday: datetime.time = None, saturday: datetime.time = None,
                               sunday: datetime.time = None):
    try:
        user_schedule = Workout_schedule(user_id=user_id, monday=monday, tuesday=tuesday, wednesday=wednesday,
                                         thursday=thursday, friday=friday, saturday=saturday, sunday=sunday)
        await user_schedule.create()
    except UniqueViolationError:
        pass


async def add_monday_workout(user_id: int, time: datetime.time):
    user_schedule = await Workout_schedule.get(user_id)
    # print(time)
    # print(type(time))
    # monday_workout = Workout_schedule(user_id=user_id, time=time)
    await user_schedule.update(monday=time).apply()


async def select_monday_workout(user_id: int, time: datetime.time):
    user_schedule = await Workout_schedule.get(user_id)
    # print(time)
    # print(type(time))
    # monday_workout = Workout_schedule(user_id=user_id, time=time)
    await user_schedule.update(monday=time).apply()


async def add_tuesday_workout(user_id: int, time: datetime.time):
    user_schedule = await Workout_schedule.get(user_id)
    # monday_workout = Workout_schedule(user_id=user_id, time=time)
    await user_schedule.update(tuesday=time).apply()


async def add_wednesday_workout(user_id: int, time: datetime.time):
    user_schedule = await Workout_schedule.get(user_id)
    # monday_workout = Workout_schedule(user_id=user_id, time=time)
    await user_schedule.update(wednesday=time).apply()


async def add_thursday_workout(user_id: int, time: datetime.time):
    user_schedule = await Workout_schedule.get(user_id)
    # monday_workout = Workout_schedule(user_id=user_id, time=time)
    await user_schedule.update(thursday=time).apply()


async def add_friday_workout(user_id: int, time: datetime.time):
    user_schedule = await Workout_schedule.get(user_id)
    # monday_workout = Workout_schedule(user_id=user_id, time=time)
    await user_schedule.update(friday=time).apply()


async def add_saturday_workout(user_id: int, time: datetime.time):
    user_schedule = await Workout_schedule.get(user_id)
    # monday_workout = Workout_schedule(user_id=user_id, time=time)
    await user_schedule.update(saturday=time).apply()


async def add_sunday_workout(user_id: int, time: datetime.time):
    user_schedule = await Workout_schedule.get(user_id)
    # monday_workout = Workout_schedule(user_id=user_id, time=time)
    await user_schedule.update(sunday=time).apply()


async def get_scheduled_day_reminders(telegram_id):
    user_schedule = select(
        [Workout_schedule.user_id, Workout_schedule.monday, Workout_schedule.tuesday, Workout_schedule.wednesday,
         Workout_schedule.thursday, Workout_schedule.friday, Workout_schedule.saturday,
         Workout_schedule.sunday]).where(Workout_schedule.user_id == telegram_id)
    us = conn.execute(user_schedule)
    return us
