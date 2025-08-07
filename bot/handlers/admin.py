from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from config.init import conf
from database.init import db
from utils.misc import try_to_int

from ..filters import FromId
from ..init import q
from ..misc import send_tech_task
from ..keyboards import kb

r = Router()
r.message.filter(
    FromId(*conf.admins),
)


@r.message(Command('help'))
async def help(msg: Message):
    await msg.answer(
        'Список команд:\n\n'

        '/id - узнать собственный id\n'
        '/list_users — список всех пользователей по ролям\n'
        '/add_manager <id> - добавить менеджера, id - id менеджера в тг\n'
        '/remove_manager <id> - удалить менеджера, id - id менеджера в тг\n'
        '/add_constructor <id> - добавить конструктора, id - id конструктора в тг\n'
        '/remove_constructor <id> - удалить конструктора, id - id конструктора в тг\n'
        '/send_task <task_id> <user_id> - отправить тз определенному пользователю с кнопкой "ответить". task_id - id ТЗ, user_id - id конструктора\n'
        '/remove_user <id> - удалить пользователя из бд, id - id в телеграме\n'
    )


@r.message(Command('send_task'))
async def send_task(msg: Message):
    params = msg.text.split(' ')

    if len(params) < 3:
        await msg.answer('Необходимо указать id тз и id получателя')
        return

    task_id = try_to_int(params[1])
    if isinstance(id, str):
        await msg.answer(f'{id} не является числом')
        return

    user_id = try_to_int(params[2])
    if isinstance(id, str):
        await msg.answer(f'{id} не является числом')
        return

    q.put(
        send_tech_task(
            user_id,
            task_id,
            kb.constructor.answer(task_id)
        )
    )
    await msg.answer('Задача добавлена в очередь!')


@r.message(Command('remove_user'))
async def remove_user(msg: Message):
    params = msg.text.split(' ')

    if len(params) == 1:
        await msg.answer('Необходимо указать id')
        return

    id = try_to_int(params[1])
    if isinstance(id, str):
        await msg.answer(f'{id} не является числом')
        return


    db.user.del_by_id(id)
    await msg.answer(f'Пользователь {id} удален!')


@r.message(Command('list_users'))
async def list_users(msg: Message):
    users = db.user.get_all()
    text = 'Все пользователи, писавшие боту:\n\n'
    index = 0

    for user in users:
        index += 1
        username = f'@{user.username}' if user.username else 'без юзернейма'
        role = user.role if user.role else 'без роли'
        text += f'{index:<2}|<code>{user.id:<11}</code>|<code>{username:<12}</code>|{role}\n'

    await msg.answer(text, parse_mode='html')


@r.message(Command('add_manager'))
async def add_manager(msg: Message):
    params = msg.text.split(' ')

    if len(params) == 1:
        await msg.answer('Необходимо указать id')
        return

    id = try_to_int(params[1])
    if isinstance(id, str):
        await msg.answer(f'{id} не является числом')
        return

    db.user.update_role(id, conf.roles.manager)
    await msg.answer(f'Пользователь {id} теперь менеджер!')


@r.message(Command('remove_manager'))
async def remove_manager(msg: Message):
    params = msg.text.split(' ')

    if len(params) == 1:
        await msg.answer('Необходимо указать id')
        return

    id = try_to_int(params[1])
    if isinstance(id, str):
        await msg.answer(f'{id} не является числом')
        return

    db.user.update_role(id, None)
    await msg.answer(f'Пользователь {id} больше не менеджер!')


@r.message(Command('add_constructor'))
async def add_consctructor(msg: Message):
    params = msg.text.split(' ')

    if len(params) == 1:
        await msg.answer('Необходимо указать id')
        return

    id = try_to_int(params[1])
    if isinstance(id, str):
        await msg.answer(f'{id} не является числом')
        return

    db.user.update_role(id, conf.roles.constructor)
    await msg.answer(f'Пользователь {id} теперь конструктор!')


@r.message(Command('remove_constructor'))
async def remove_constructor(msg: Message):
    params = msg.text.split(' ')

    if len(params) == 1:
        await msg.answer('Необходимо указать id')
        return

    id = try_to_int(params[1])
    if isinstance(id, str):
        await msg.answer(f'{id} не является числом')
        return

    db.user.update_role(id, None)
    await msg.answer(f'Пользователь {id} больше не конструктор!')
