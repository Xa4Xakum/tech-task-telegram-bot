from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from loguru import logger

from config.init import conf
from database.init import db

from ...keyboards import kb
from ...filters import ChatType, Role
from ...states import ConstructorStates, EditAnswerStates
from ...misc import parse_datetime, correct_date_example

r = Router()
r.message.filter(
    ChatType('private'),
    Role(conf.roles.constructor)
)


@r.message(
    F.text == kb.btn.constructor.continue_edit.text,
    StateFilter(EditAnswerStates)
)
@r.message(
    F.text == kb.btn.edit.text,
    ConstructorStates.tasks_history
)
async def edit(msg: Message, state: FSMContext):
    await msg.answer('Что вы хотели бы изменить?', reply_markup=kb.constructor.edit_answer)
    await state.set_state(EditAnswerStates.get_subject)


@r.message(
    F.text == kb.btn.deadline.text,
    EditAnswerStates.get_subject
)
async def deadline(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    answer = db.answer.get_by_ids(task_id, msg.from_user.id)
    await msg.answer(
        f"Отправьте новый дедлайн в формате ДД.ММ.ГГГГ ЧЧ:ММ\n"
        f'Текущий дедлайн: <code>{answer.deadline.strftime(conf.datetime_format)}</code>',
        parse_mode='html'
    )
    await state.set_state(EditAnswerStates.get_deadline)


@r.message(EditAnswerStates.get_deadline)
async def get_deadline(msg: Message, state: FSMContext):
    date = parse_datetime(msg.text, conf.datetime_format)
    if not date:
        await msg.answer(
            f'Не удалось спарсить дату из {msg.text}, попробуйте еще раз. '
            f'Пример правильной даты: <code>{correct_date_example()}</code>',
            parse_mode='html'
        )
        return

    data = await state.get_data()
    task_id = data.get('task_id')
    db.answer.update_deadline(task_id, msg.from_user.id, date)
    await msg.answer('Обновлено!', reply_markup=kb.constructor.after_edit_answer)


@r.message(
    F.text == kb.btn.constructor.price.text,
    EditAnswerStates.get_subject
)
async def price(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    answer = db.answer.get_by_ids(task_id, msg.from_user.id)
    await msg.answer(
        f"Отправьте новую цену\n"
        f'Текущая цена: <code>{answer.price}</code>',
        parse_mode='html'
    )
    await state.set_state(EditAnswerStates.get_price)


@r.message(EditAnswerStates.get_price)
async def get_price(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    db.answer.update_price(task_id, msg.from_user.id, msg.text)
    await msg.answer('Обновлено!', reply_markup=kb.constructor.after_edit_answer)


@r.message(
    F.text == kb.btn.constructor.comment.text,
    EditAnswerStates.get_subject
)
async def comment(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    answer = db.answer.get_by_ids(task_id, msg.from_user.id)
    await msg.answer(
        f"Отправьте новый комментарий\n"
        f'Текущий комментарий:\n\n<code>{answer.text}</code>',
        parse_mode='html'
    )
    await state.set_state(EditAnswerStates.get_comment)


@r.message(EditAnswerStates.get_comment)
async def get_comment(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    db.answer.update_comment(task_id, msg.from_user.id, msg.text)
    await msg.answer('Обновлено!', reply_markup=kb.constructor.after_edit_answer)

