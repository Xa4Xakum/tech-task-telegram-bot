from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from config.init import conf
from database.init import db

from ...keyboards import kb
from ...filters import ChatType, Role
from ...states import ManagerStates
from ...misc import parse_datetime, send_task_answer, correct_date_example, try_send_message

r = Router()
r.message.filter(
    ChatType('private'),
    Role(conf.roles.manager)
)
r.callback_query.filter(
    Role(conf.roles.manager)
)

@r.message(F.text == 'err')
async def err(msg: Message, state: FSMContext):
    await msg.answer(str(10 / 0))


@r.callback_query(F.data.startswith('answer'))
async def answer_callback(call: CallbackQuery, state: FSMContext):
    task_id = int(call.data.split(':')[1])
    user_id = int(call.data.split(':')[2])
    task = db.tech_task.get_by_id(task_id)

    if not task:
        await call.message.answer(f'ТЗ не найдено, возможно оно было удалено')
        return
    await state.update_data(user_id=user_id, task=task)

    await call.message.answer(f'Отправьте ваш ответ', reply_markup=kb.constructor.choose_action)
    await state.set_state(ManagerStates.answer_question)


@r.message(
    ManagerStates.answer_question
)
async def answer_question(msg: Message, state: FSMContext):
    data = await state.get_data()
    task = data.get('task')
    user_id = data.get('user_id')

    rmsg = await try_send_message(
        chat_id=user_id,
        text=(
            f'Ответ на ваш вопрос по ТЗ #{task.create_at.strftime(conf.task_date_identifire_format)}\n\n'
            f'{msg.text}'
        )
    )
    if not rmsg:
        await msg.answer('Не удалось отправить ваш ответ... возможно конструктор был удален или запретил боту писать сообщения.')
        return

    await msg.answer(
        'Ваш ответ доставлен!',
        reply_markup=kb.to_menu
    )
