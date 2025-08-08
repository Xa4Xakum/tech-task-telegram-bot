from aiogram.fsm.state import StatesGroup, State


class ManagerStates(StatesGroup):
    get_task_text = State()
    get_media = State()
    get_deadline = State()
    get_recievers = State()

    tasks_history = State()
    task_answers = State()
    confirm = State()

class ConstructorStates(StatesGroup):
    opened_tasks = State()
    tasks_history = State()
    get_price = State()
    get_deadline = State()
    get_com = State()


class EditAnswerStates(StatesGroup):
    get_subject = State()
    get_deadline = State()
    get_price = State()
    get_comment = State()
