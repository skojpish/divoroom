from aiogram.fsm.state import StatesGroup, State

# Set states
class IdeaState(StatesGroup):
    idea = State()
    edit = State()

class DescripState(StatesGroup):
    description = State()
    edit = State()

class CityState(StatesGroup):
    city = State()
    edit = State()

class FullNameState(StatesGroup):
    full_name = State()
    edit = State()

class NumberState(StatesGroup):
    number = State()
    edit = State()


















