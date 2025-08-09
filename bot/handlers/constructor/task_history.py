from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from loguru import logger

from config.init import conf
from utils.misc import try_to_int
from database.init import db

from ...keyboards import kb
from ...filters import ChatType, Role
from ...states import ConstructorStates
from ...misc import send_tech_task, send_task_answer

r = Router()
r.message.filter(
    ChatType('private'),
    Role(conf.roles.constructor)
)


@r.message(
    F.text == kb.btn.next.text,
    StateFilter(ConstructorStates.tasks_history)
)
async def next(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_index: int = data.get('task_index', 0)
    await state.update_data(task_index=task_index+1)
    await send_corusel(msg, state)


@r.message(
    F.text == kb.btn.previous.text,
    StateFilter(ConstructorStates.tasks_history)
)
async def previous(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_index: int = data.get('task_index', 0)
    await state.update_data(task_index=task_index-1)
    await send_corusel(msg, state)


@r.message(
    F.text.in_([
        kb.btn.constructor.tasks_history.text,
        kb.btn.to_history.text
    ])
)
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
    user_answer = db.answer.get_by_ids(task_id=task.id, user_id=user_id)
    start_text = f'{task_index + 1}/{len(tasks)}\n'

    if not user_answer:
        start_text += '❌Вы не ответили на ТЗ\n\n'
        if task.deadline > datetime.now(): markup = kb.constructor.corusel_with_answer
        else: markup = kb.corusel
    else:
        start_text += '✅Вы ответили на ТЗ\n\n'
        markup = kb.constructor.corusel_with_show_answer
        
    await state.update_data(task_index=task_index, task_id=task.id)
    await state.set_state(ConstructorStates.tasks_history)
    await send_tech_task(
        user_id,
        task.id,
        reply_markup=markup,
        start_text=start_text
    )


@r.message(
    F.text == kb.btn.constructor.show_answer.text,
    StateFilter(ConstructorStates.tasks_history)
)
async def show_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    task = db.tech_task.get_by_id(task_id)

    if not task:
        await msg.answer('Кажется кто-то только что удалил ТЗ.. Если проблема повторится - напишите менеджеру')
        return

    await send_task_answer(
        msg.from_user.id,
        task.id,
        msg.from_user.id,
        reply_markup=kb.corusel_with_edit
    )
