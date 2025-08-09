from aiogram.fsm.state import StatesGroup, State


# ----- Стейты менеджера -----

class CreateTaskStates(StatesGroup):
    get_task_text = State()
    get_media = State()
    get_deadline = State()
    get_recievers = State()
    confirm = State()


class EditTaskStates(StatesGroup):
    get_subject = State()
    get_task_text = State()
    get_media = State()
    get_deadline = State()


class ManagerStates(StatesGroup):
    get_tasks_owner = State()
    tasks_history = State()
    task_answers = State()


# ----- Стейты конструктора -----

class ConstructorStates(StatesGroup):
    opened_tasks = State()
    tasks_history = State()


class CreateAnswerStates(StatesGroup):
    get_price = State()
    get_deadline = State()
    get_com = State()


class EditAnswerStates(StatesGroup):
    get_subject = State()
    get_deadline = State()
    get_price = State()
    get_comment = State()
