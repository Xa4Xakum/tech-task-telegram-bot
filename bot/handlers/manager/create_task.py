import asyncio
from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import KeyboardButton
from loguru import logger

from config.init import conf
from utils.misc import extract_media_info, try_to_int
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


@r.message(F.text == kb.btn.manager.create_task.text)
async def start_create_task(msg: Message, state: FSMContext):
    await msg.answer("📝 Введите текст задания:", reply_markup=kb.cancel)
    await state.set_state(ManagerStates.get_task_text)


# 🧾 Получение текста
@r.message(ManagerStates.get_task_text)
async def get_task_text(msg: Message, state: FSMContext):
    await state.update_data(text=msg.text, media=[])
    await msg.answer(
        "📎 Теперь отправьте файлы (фото, видео, голосовые, документы). Когда закончите — нажмите на кнопку.\n"
        'ВАЖНО! Не отправляйте одно и то же вложение дважды - сохранится только одна копия',
        reply_markup=kb.ready
    )
    await state.set_state(ManagerStates.get_media)


# 🖼️ Получение медиа
@r.message(F.content_type.in_(["photo", "video", "voice", "document"]), ManagerStates.get_media)
async def get_media(msg: Message, state: FSMContext):
    data = await state.get_data()
    media = data.get("media", [])
    media.append(msg)  # сохраняем весь объект Message, ты потом сам вытащишь file_id и тип
    await state.update_data(media=media)


# ✅ пропуск медиа
@r.message(
    F.text == kb.btn.skip.text,
    ManagerStates.get_media
)
async def skip_media(msg: Message, state: FSMContext):
    await msg.answer(
        "🕒 Укажи дедлайн в формате `ДД.ММ.ГГГГ ЧЧ:ММ`\n"
        f'Пример правильной даты: {datetime.now().strftime("%d.%m.%Y %H:%M")}'
    )
    await state.set_state(ManagerStates.get_deadline)


# ✅ Завершение медиа
@r.message(
    F.text == kb.btn.ready.text,
    ManagerStates.get_media
)
async def done_media(msg: Message, state: FSMContext):
    data = await state.get_data()
    media = data.get("media", [])
    if len(media) == 0:
        await msg.answer(
            'Вы не добавили ни одного вложения',
            reply_markup=kb.ready
        )
        return
    await skip_media(msg, state)


# 🕒 Дедлайн
@r.message(ManagerStates.get_deadline)
async def get_deadline(msg: Message, state: FSMContext):
    date = parse_datetime(msg.text, "%d.%m.%Y %H:%M")
    if not date:
        await msg.answer(
            f'Не удалось спарсить дату из {msg.text}, попробуйте еще раз. '
            f'Пример правильной даты: {datetime.now().strftime("%d.%m.%Y %H:%M")}'
        )
        return

    await state.update_data(deadline=date)
    users = db.user.get_all_with_role(conf.roles.constructor)
    btns = [kb.btn.skip, kb.btn.ready]
    text = 'Выберите получателей(нажмите готово, когда выберете всех):\n'

    for user in users:
        btns.append(KeyboardButton(text=str(user.id)))
        text += f'- {user.id:<11} - @{user.username}\n'
        
    await msg.answer(text, reply_markup=kb.reply_markup_from_buttons(*btns, adjust=[2]))
    await state.set_state(ManagerStates.get_recievers)


@r.message(
    F.text.not_in([
        kb.btn.skip.text,
        kb.btn.ready.text
    ]),
    ManagerStates.get_recievers
)
async def get_recievers(msg: Message, state: FSMContext):
    user_id = try_to_int(msg.text)

    if isinstance(user_id, str):
        await msg.answer(f'{user_id} не является числом')
        return

    user = db.user.get_by_id(user_id)

    if user.role != conf.roles.constructor:
        await msg.answer(f'Пользователь {user.id}(@{user.username}) не является конструктором')
        return

    data = await state.get_data()
    user_ids = data.get('user_ids', [])
    user_ids.append(user_id)

    await state.update_data(user_ids=user_ids)


@r.message(F.text == kb.btn.ready.text, ManagerStates.get_recievers)
async def ready_get_recievers(msg: Message, state: FSMContext):
    data = await state.get_data()
    users = data.get('user_ids', [])

    if len(users) == 0:
        await msg.answer('Вы не добавили ни одного пользователя')
        return

    await check(msg, state)


@r.message(F.text == kb.btn.skip.text, ManagerStates.get_recievers)
async def check(msg: Message, state: FSMContext):

    data = await state.get_data()
    text = data["text"]
    recievers = data.get('user_ids', None)
    recievers_as_text = 'Все конструкторы'

    if recievers:
        recievers_as_text = '\n'
        for i in recievers:
            user = db.user.get_by_id(i)
            recievers_as_text += f'- {user.id:<11} - @{user.username}\n'

    await msg.answer(
        f"📌 Проверь:\n\n"
        f"<b>Текст:</b>\n{text}\n\n"
        f"<b>Медиа:</b> {len(data.get('media', []))} файла(ов)\n"
        f"<b>Оценить до:</b> {data['deadline']}\n"
        f'<b>Получатели:</b> {recievers_as_text}',
        parse_mode="HTML",
        reply_markup=kb.check
    )
    await state.set_state(ManagerStates.confirm)


# ☑️ Подтверждение
@r.message(F.text == kb.btn.all_good.text, ManagerStates.confirm)
async def confirm_task(msg: Message, state: FSMContext):
    data = await state.get_data()
    text = data["text"]
    deadline = data["deadline"]
    owner_id = msg.from_user.id
    media: list[Message] = data.get("media", [])

    task = db.tech_task.add(
        text=text,
        owner_id=owner_id,
        deadline=deadline,
        status=conf.task_statuses.open
    )
    added = []
    for i in media:
        for j in extract_media_info(i):
            logger.debug(j)
            if j not in added:
                db.media.add(
                    task_id=task.id,
                    file_id=j["file_id"],
                    media_type=j["media_type"],
                )
                added.append(j)

    await msg.answer(
        f"✅ Техническое задание #{task.id} создано!",
        reply_markup=kb.to_menu
    )
    await state.clear()
    q.put(mail_task(task.id, data.get('user_ids', None)))


async def mail_task(task_id: int, users: list[int] | None = None):
    if not users: users = [i.id for i in db.user.get_all_with_role(conf.roles.constructor)]
    for user in users:
        await send_tech_task(
            user,
            task_id,
            kb.constructor.answer(task_id)
        )
        await asyncio.sleep(2)
