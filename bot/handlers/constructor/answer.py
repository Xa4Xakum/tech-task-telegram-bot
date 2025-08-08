from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from config.init import conf
from utils.misc import try_to_int
from database.init import db

from ...keyboards import kb
from ...filters import ChatType, Role
from ...states import ConstructorStates
from ...misc import parse_datetime, send_task_answer

r = Router()
r.message.filter(
    ChatType('private'),
    Role(conf.roles.constructor)
)


@r.message(
    F.text == kb.btn.constructor.answer_reply.text,
    StateFilter(ConstructorStates.tasks_history)
)
async def answer_reply(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')

    if not task_id:
        await msg.answer('Странно.. я забыл id ТЗ, напишите об этом менеджеру')
        return

    answer = db.answer.get_by_ids(task_id, msg.from_user.id)
    if answer:
        await msg.answer('Вы уже ответили на это ТЗ')
        return

    await msg.answer(f'Отправьте примерную стоимость выполнения ТЗ')
    await state.set_state(ConstructorStates.get_price)


@r.callback_query(F.data.startswith('answer'))
async def answer_callback(call: CallbackQuery, state: FSMContext):
    task_id = int(call.data.split(':')[1])
    task = db.tech_task.get_by_id(task_id)

    if not task:
        await call.message.answer(f'ТЗ #{task_id} не найдено, возможно оно было удалено')
        return

    answer = db.answer.get_by_ids(task_id, call.from_user.id)
    if answer:
        await call.answer('Вы уже ответили на это тз')
        return

    await call.message.answer(f'Отправьте примерную стоимость выполнения ТЗ')
    await state.update_data(task_id=task_id)
    await state.set_state(ConstructorStates.get_price)


@r.message(StateFilter(ConstructorStates.get_price))
async def get_price(msg: Message, state: FSMContext):
    price = try_to_int(msg.text)
    if not isinstance(price, int):
        await msg.answer(f'{price} не является числом, попробуйте еще раз.')
        return

    await msg.answer(
        f'Оцените срок выполнения. Отправьте дату окончания выполнения в формате ДД.ММ.ГГГГ ЧЧ:ММ'
        f'Пример правильной даты: {datetime.now().strftime("%d.%m.%Y %H:%M")}'
    )
    await state.update_data(price=price)
    await state.set_state(ConstructorStates.get_deadline)


@r.message(StateFilter(ConstructorStates.get_deadline))
async def get_deadline(msg: Message, state: FSMContext):
    date = parse_datetime(msg.text, "%d.%m.%Y %H:%M")
    if not date:
        await msg.answer(
            f'Не удалось спарсить дату из {msg.text}, попробуйте еще раз. '
            f'Пример правильной даты: <code>{datetime.now().strftime("%d.%m.%Y %H:%M")}</code>',
            parse_mode='html'
        )
        return

    await msg.answer(
        f'Хотите добавить комментарий? Напишите его, либо нажмите на кнопку',
        reply_markup=kb.constructor.without_com
    )
    await state.update_data(date=date)
    await state.set_state(ConstructorStates.get_com)


@r.message(StateFilter(ConstructorStates.get_com))
async def get_com(msg: Message, state: FSMContext):
    com = msg.text
    data = await state.get_data()

    task = db.tech_task.get_by_id(data['task_id'])
    if not task:
        await msg.answer(f'ТЗ #{task.id} не найдено, возможно оно было удалено')
        await state.clear()
        return

    db.answer.add(
        task_id=data['task_id'],
        user_id=msg.from_user.id,
        text=com,
        price=data['price'],
        deadline=data['date']
    )
    await send_task_answer(task.owner_id, task.id, msg.from_user.id)
    await msg.answer(
        f'Ваш ответ добавлен!',
        reply_markup=kb.to_menu
    )
    await state.clear()
