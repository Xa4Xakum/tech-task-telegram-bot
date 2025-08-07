from aiogram.fsm.state import StatesGroup, State


class ManagerStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_media = State()
    waiting_for_deadline = State()
    tasks_history = State()
    task_answers = State()
    confirm = State()

class ConstructorStates(StatesGroup):
    opened_tasks = State()
    tasks_history = State()
    get_price = State()
    get_deadline = State()
    get_com = State()
