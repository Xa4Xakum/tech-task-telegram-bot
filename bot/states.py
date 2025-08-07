from aiogram.fsm.state import StatesGroup, State


class CreateTaskStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_media = State()
    waiting_for_deadline = State()
    confirm = State()

class ConstructorStates(StatesGroup):
    opened_tasks = State()
    tasks_history = State()
    get_price = State()
    get_deadline = State()
    get_com = State()
