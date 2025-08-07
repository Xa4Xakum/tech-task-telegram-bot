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
from ...states import CreateTaskStates
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
    await state.set_state(CreateTaskStates.waiting_for_text)


# 🧾 Получение текста
@r.message(CreateTaskStates.waiting_for_text)
async def get_task_text(msg: Message, state: FSMContext):
    await state.update_data(text=msg.text, media=[])
    await msg.answer(
        "📎 Теперь отправьте файлы (фото, видео, голосовые, документы). Когда закончите — нажмите на кнопку.\n"
        'ВАЖНО! Не отправляйте одно и то же вложение дважды - сохранится только одна копия',
        reply_markup=kb.ready
    )
    await state.set_state(CreateTaskStates.waiting_for_media)


# 🖼️ Получение медиа
@r.message(F.content_type.in_(["photo", "video", "voice", "document"]), CreateTaskStates.waiting_for_media)
async def get_media(msg: Message, state: FSMContext):
    data = await state.get_data()
    media = data.get("media", [])
    media.append(msg)  # сохраняем весь объект Message, ты потом сам вытащишь file_id и тип
    await state.update_data(media=media)


# ✅ пропуск медиа
@r.message(
    F.text == kb.btn.skip.text,
    CreateTaskStates.waiting_for_media
)
async def skip_media(msg: Message, state: FSMContext):
    await msg.answer(
        "🕒 Укажи дедлайн в формате `ДД.ММ.ГГГГ ЧЧ:ММ`\n"
        f'Пример правильной даты: {datetime.now().strftime("%d.%m.%Y %H:%M")}'
    )
    await state.set_state(CreateTaskStates.waiting_for_deadline)


# ✅ Завершение медиа
@r.message(
    F.text == kb.btn.ready.text,
    CreateTaskStates.waiting_for_media
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
@r.message(CreateTaskStates.waiting_for_deadline)
async def get_deadline(msg: Message, state: FSMContext):
    date = parse_datetime(msg.text, "%d.%m.%Y %H:%M")
    if not date:
        await msg.answer(
            f'Не удалось спарсить дату из {msg.text}, попробуйте еще раз. '
            f'Пример правильной даты: {datetime.now().strftime("%d.%m.%Y %H:%M")}'
        )
        return
    # Тут можешь сам парсить дату и валидировать
    await state.update_data(deadline=date)

    data = await state.get_data()
    text = data["text"]

    await msg.answer(
        f"📌 Проверь:\n\n"
        f"<b>Текст:</b>\n{text}\n\n"
        f"<b>Медиа:</b> {len(data.get('media', []))} файла(ов)\n"
        f"<b>Оценить до:</b> {date}",
        parse_mode="HTML",
        reply_markup=kb.check
    )
    await state.set_state(CreateTaskStates.confirm)


# ☑️ Подтверждение
@r.message(F.text == kb.btn.all_good.text, CreateTaskStates.confirm)
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
    q.put(mail_task(task.id))


async def mail_task(task_id: int):
    users = db.user.get_all_with_role(conf.roles.constructor)
    for user in users:
        await send_tech_task(
            user.id,
            task_id,
            kb.constructor.answer(task_id)
        )
        await asyncio.sleep(2)
