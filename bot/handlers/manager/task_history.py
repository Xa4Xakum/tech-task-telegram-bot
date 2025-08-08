import asyncio
from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

from config.init import conf
from utils.misc import extract_media_info
from database.init import db

from ...keyboards import kb
from ...filters import ChatType, Role
from ...states import ManagerStates
from ...misc import send_tech_task, parse_datetime
from ...init import q

r = Router()
r.message.filter(
    ChatType('private'),
    Role(conf.roles.manager)
)


@r.message(
    F.text == kb.btn.next.text,
    StateFilter(ManagerStates.tasks_history)
)
async def next(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_index: int = data.get('task_index', 0)
    await state.update_data(task_index=task_index+1)
    await send_corusel(msg, state)


@r.message(
    F.text == kb.btn.previous.text,
    StateFilter(ManagerStates.tasks_history)
)
async def previous(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_index: int = data.get('task_index', 0)
    await state.update_data(task_index=task_index-1)
    await send_corusel(msg, state)


@r.message(
    F.text == kb.btn.manager.back_to_tasks.text,
    StateFilter(ManagerStates.task_answers)
)
@r.message(F.text == kb.btn.manager.tasks_history.text)
async def send_corusel(msg: Message, state: FSMContext):
    tasks = db.tech_task.get_all()

    if len(tasks) == 0:
        await msg.answer('На моей памяти не было ни одного ТЗ...')
        return

    data = await state.get_data()
    task_index: int = data.get('task_index', 0)

    if task_index >= len(tasks): task_index = 0
    if task_index < 0: task_index = len(tasks) - 1

    task = tasks[task_index]
    user_id = msg.from_user.id
    answers = db.answer.get_by_task(task_id=task.id)
    avarage = 0
    answers_text = "Оценки:\n"
    for i in answers:
        user = db.user.get_by_id(i.user_id)
        username = user.username if user else None
        if not username: username = i.user_id

        answers_text += f'<i>{username:<11} - до {i.deadline.strftime(conf.datetime_format)} за {i.price}</i>\n'
    if avarage != 0: avarage = round(avarage / len(answers), 2)

    start_text = (
        f'{task_index + 1}/{len(tasks)}\n'
        f'Кол-во ответов: {len(answers)}\n'
        f'{answers_text}\n'
    )

    if len(answers) > 0: markup = kb.manager.opened_tasks_corusel_with_show_answers
    else: markup = kb.corusel
        
    await state.update_data(task_index=task_index, task_id=task.id)
    await state.set_state(ManagerStates.tasks_history)
    await send_tech_task(
        user_id,
        task.id,
        reply_markup=markup,
        start_text=start_text
    )
