from dataclasses import dataclass

from aiogram.dispatcher.filters.state import StatesGroup, State


class Set_program(StatesGroup):
    program_name = State()
    program_is_free = State()
    morning_program = State()
    level_program = State()
    sex_program = State()
    age_program = State()
    random_workout = State()


class Set_exercise(StatesGroup):
    exercise_name = State()
    exercise_duration = State()
    exercise_definition = State()
    exercise_file = State()


@dataclass
class Exercise:
    exercise_id: int
    exercise_name: str
    exercise_duration: int
    exercise_definition: str
    exercise_file: str


program_types = {1: "Ранкова", 2: "Періодична", 3: "Разова", 4: "", 5: "Інші"}

level_program = {1: "low", 2: "medium", 3: "high"}
level_program_eng_ukr = {"any": "Будь-який рівень", "low": "Початковий рівень", "medium": "Середній рівень",
                         "high": "Професіональний рівень"}

sex = {"None": "Будь-яка стать", "male": "Чоловіча", "female": "Жіноча"}

age = {0: "Новонароджений", 4: "Немовля", 8: "Дитина", 12: "", 16: "Підліток", 25: "Юнак", 35: "Дорослий", 45: "",
       60: "Похилого віку"}

age2 = {"None": "Будь-який вік", 1: "4-8", 2: "8-12", 3: "12-16", 4: "16-25", 5: "25-35", 6: "35-45", 7: "45-60",
        8: "60+"}
