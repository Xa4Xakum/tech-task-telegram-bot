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
from ...misc import send_task_answer
from ...init import q

r = Router()
r.message.filter(
    ChatType('private'),
    Role(conf.roles.manager)
)


@r.message(
    F.text == kb.btn.manager.show_answers.text,
    StateFilter(ManagerStates.tasks_history)
)
async def task_history(msg: Message, state: FSMContext):
    await send_corusel(msg, state)


@r.message(
    F.text == kb.btn.next.text,
    StateFilter(ManagerStates.task_answers)
)
async def next(msg: Message, state: FSMContext):
    data = await state.get_data()
    answer_index: int = data.get('answer_index', 0)
    await state.update_data(answer_index=answer_index+1)
    await send_corusel(msg, state)


@r.message(
    F.text == kb.btn.previous.text,
    StateFilter(ManagerStates.task_answers)
)
async def previous(msg: Message, state: FSMContext):
    data = await state.get_data()
    answer_index: int = data.get('answer_index', 0)
    await state.update_data(answer_index=answer_index-1)
    await send_corusel(msg, state)


async def send_corusel(msg: Message, state: FSMContext):

    data = await state.get_data()
    answer_index: int = data.get('answer_index', 0)
    task_id = data.get('task_id')

    if not task_id:
        await msg.answer(f'Не могу вспомнить тз, о котором мы говорили... Напишите менеджеру об этой проблеме')
        return

    answers = db.answer.get_by_task(task_id)

    if len(answers) == 0:
        await msg.answer(f'На моей памяти не было ни одного ответа на это ТЗ...')
        return

    if answer_index >= len(answers): answer_index = 0
    if answer_index < 0: answer_index = len(answers) - 1

    markup = kb.manager.corusel_with_back_to_tasks
    answer = answers[answer_index]
    start_text = f'{answer_index + 1}/{len(answers)}\n\n'
        
    await state.update_data(answer_index=answer_index, task_id=task_id)
    await state.set_state(ManagerStates.task_answers)
    await send_task_answer(
        msg.from_user.id,
        task_id,
        answer.user_id,
        start_text,
        markup
    )