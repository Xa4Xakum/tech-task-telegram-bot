from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from loguru import logger

from config.init import conf
from database.init import db
from utils.misc import extract_media_info, try_to_int

from ...keyboards import kb
from ...filters import ChatType, Role
from ...states import ManagerStates, EditTaskStates
from ...misc import parse_datetime, correct_date_example

r = Router()
r.message.filter(
    ChatType('private'),
    Role(conf.roles.manager)
)


@r.message(
    F.text == kb.btn.continue_edit.text,
    StateFilter(EditTaskStates)
)
@r.message(
    F.text == kb.btn.edit.text,
    ManagerStates.tasks_history
)
async def edit(msg: Message, state: FSMContext):
    await msg.answer('Что вы хотели бы изменить?', reply_markup=kb.manager.edit_task)
    await state.set_state(EditTaskStates.get_subject)


@r.message(
    F.text == kb.btn.deadline.text,
    EditTaskStates.get_subject
)
async def deadline(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    task = db.tech_task.get_by_id(task_id)
    await msg.answer(
        f"Отправьте новый дедлайн в формате ДД.ММ.ГГГГ ЧЧ:ММ\n"
        f'Текущий дедлайн: <code>{task.deadline.strftime(conf.datetime_format)}</code>',
        parse_mode='html'
    )
    await state.set_state(EditTaskStates.get_deadline)


@r.message(EditTaskStates.get_deadline)
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
    db.tech_task.update_deadline(task_id, date)
    await msg.answer('Обновлено!', reply_markup=kb.after_edit)


@r.message(
    F.text == kb.btn.manager.text.text,
    EditTaskStates.get_subject
)
async def text(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    task = db.tech_task.get_by_id(task_id)
    await msg.answer(
        f"Отправьте новый текст ТЗ\n"
        f'Текущий текст:\n\n<code>{task.text}</code>',
        parse_mode='html'
    )
    await state.set_state(EditTaskStates.get_task_text)


@r.message(EditTaskStates.get_task_text)
async def get_task_text(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    db.tech_task.update_text(task_id, msg.text)
    await msg.answer('Обновлено!', reply_markup=kb.after_edit)


@r.message(
    F.text == kb.btn.manager.attachments.text,
    EditTaskStates.get_subject
)
async def attachments(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    task = db.tech_task.get_by_id(task_id)
    await msg.answer(
        f"Отправьте новые вложения\n"
        f'Сейчас добавлено файлов: <code>{len(task.media)}</code>',
        parse_mode='html',
        reply_markup=kb.manager.edit_attachments
    )
    await state.set_state(EditTaskStates.get_media)


# 🖼️ Получение медиа
@r.message(F.content_type.in_(["photo", "video", "voice", "document"]), EditTaskStates.get_media)
async def get_media(msg: Message, state: FSMContext):
    data = await state.get_data()
    media = data.get("media", [])
    media.append(msg)
    await state.update_data(media=media)


# ✅ Завершение медиа
@r.message(
    F.text == kb.btn.ready.text,
    EditTaskStates.get_media
)
async def done_media(msg: Message, state: FSMContext):
    data = await state.get_data()
    media = data.get("media", [])
    if len(media) == 0:
        await msg.answer(
            'Вы не добавили ни одного вложения',
        )
        return
    await replace_media(msg, state)

@r.message(
    F.text == kb.btn.manager.del_attachments.text,
    EditTaskStates.get_media
)
async def replace_media(msg: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    media: list[Message] = data.get("media", [])

    db.media.del_by_task(task_id)
    added = []

    for i in media:
        for j in extract_media_info(i):
            logger.debug(j)
            if j not in added:
                db.media.add(
                    task_id=task_id,
                    file_id=j["file_id"],
                    media_type=j["media_type"],
                )
                added.append(j)

    await state.update_data(media=[])
    await msg.answer('Обновлено!', reply_markup=kb.after_edit)
