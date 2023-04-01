
from aiogram.fsm.state import StatesGroup, State

class UserNumbers(StatesGroup):
    random_numb = State()
    user_number = State()
