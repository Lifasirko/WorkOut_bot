from aiogram.dispatcher.filters.state import StatesGroup, State


# Создаем группу состояний Test - для тестирования.
# Если у вас другой смысл состояний - называйте соответственно, не надо тупо копировать Test
class Registration_states(StatesGroup):
    # Создаем состояние в этой группе. Называйте каждое состояние соответственно его назначению.
    # В данном случае Q1 - question 1, то есть первый вопрос. У вас это может быть по-другому
    Not_registered = State()
    Registered = State()
