import asyncio
from datetime import datetime, timedelta

from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaDocument,
    Message
)
from aiogram.utils.formatting import (
    Bold, Text
)
from loguru import logger

from database.init import db
from utils.try_do import try_do
from config.init import conf

from .keyboards import kb
from .init import bot


def correct_date_example():
    return (datetime.now() + timedelta(hours=4)).strftime(conf.datetime_format)


@try_do(1, 'warning')
async def deadline_notify():
    logger.info('Запущена задача на уведомление о просрочке ответа')
    tasks = db.tech_task.get_with_deadline_smaller_than(datetime.now() + timedelta(minutes=30))
    users = db.user.get_all_with_role(conf.roles.constructor)
    for task in tasks:
        left = task.deadline - datetime.now()
        left = int(left.seconds / 60) 
        for user in users:
            answer = db.answer.get_by_ids(task.id, user.id)
            if not answer:
                logger.info(f'Пользователь {user.id} не ответил на ТЗ, отправка уведомления...')
                await send_tech_task(
                    chat_id=user.id,
                    task_id=task.id,
                    reply_markup=kb.constructor.answer(task.id),
                    start_text=f'Вы не ответили на это тз, у вас осталось {left} минут!\n\n'
                )
                await asyncio.sleep(2)


@try_do(1, 'warning')
def parse_datetime(string: str, format: str = "%d.%m.%Y %H:%M"):
    return datetime.strptime(string, format)


@try_do(1, 'warning')
async def del_msg(msg: Message):
    await msg.delete()


@try_do(1, 'warning')
async def send_task_answer(
    chat_id: int,
    task_id: int,
    user_id: int,
    start_text: str = '',
    reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None,
):
    answer = db.answer.get_by_ids(task_id, user_id)
    user = db.user.get_by_id(user_id)
    task = db.tech_task.get_by_id(task_id)
    text = Text(
        start_text,
        Bold(f"ТЗ #{task_id}\n"),
        Bold(f"Дата создания:"), f"{task.create_at.strftime("%d.%m.%Y %H:%M")}\n",
        Bold(f"Ответ от:"), f"{user.id}(@{user.username})\n",
        f'Сможет выполнить до {answer.deadline.strftime("%d.%m.%Y %H:%M")} за {answer.price}\n\n',
        answer.text
    )
    await bot.send_message(
        chat_id=chat_id,
        reply_markup=reply_markup,
        **text.as_kwargs()
    )


@try_do(1, 'warning')
async def send_tech_task(
    chat_id: int,
    task_id: int,
    reply_markup: None | InlineKeyboardMarkup | ReplyKeyboardMarkup = None,
    start_text: str = '',
):
    task = db.tech_task.get_by_id(task_id)
    if not task:
        raise ValueError(f"Task {task_id} not found")

    text = Text(
        start_text,
        Bold(f'ТЗ #{task.id} от {task.create_at.strftime("%d.%m.%Y %H:%M")}\n'),
        Bold(f'Нужен ответ до {task.deadline.strftime("%d.%m.%Y %H:%M")}\n\n'),
        task.text
    )

    # 1. Отправляем текст
    await bot.send_message(
        chat_id=chat_id,
        reply_markup=reply_markup,
        **text.as_kwargs()
    )

    if not task.media:
        return

    # 2. Группировка по типу
    grouped = {
        "photo": [],
        "video": [],
        "document": [],
        "audio": [],
        "voice": [],
    }

    for m in task.media:
        if m.media_type in grouped:
            grouped[m.media_type].append(m.file_id)
        else:
            logger.warning(f"Неизвестный тип вложения: {m.media_type}")

    # 3. Отправка в группах
    for mtype, items in grouped.items():
        if not items:
            continue

        # Формируем media группы (по 10 максимум)
        if mtype == "photo":
            batches = [items[i:i + 10] for i in range(0, len(items), 10)]
            for batch in batches:
                media = [InputMediaPhoto(media=str(f)) for f in batch]
                await bot.send_media_group(chat_id, media)

        elif mtype == "video":
            batches = [items[i:i + 10] for i in range(0, len(items), 10)]
            for batch in batches:
                media = [InputMediaVideo(media=str(f)) for f in batch]
                await bot.send_media_group(chat_id, media)

        elif mtype == "document":
            batches = [items[i:i + 10] for i in range(0, len(items), 10)]
            for batch in batches:
                media = [InputMediaDocument(media=str(f)) for f in batch]
                await bot.send_media_group(chat_id, media)

        # audio и voice — по одному
        elif mtype == "audio":
            for f in items:
                await bot.send_audio(chat_id, str(f))

        elif mtype == "voice":
            for f in items:
                await bot.send_voice(chat_id, str(f))
