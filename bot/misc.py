from datetime import datetime

from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaDocument,
    Message
)
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag, Text, Italic
)
from loguru import logger

from database.init import db
from utils.try_do import try_do

from .init import bot

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
    text = Text(
        start_text,
        Bold(f"Ответ от {user.id}(@{user.username}) на ТЗ #{task_id}\n"),
        f'До {answer.deadline.strftime("%d.%m.%Y %H:%M")} за {answer.price}\n\n',
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
        Bold(f'ТЗ #{task.id}, нужен ответ до {task.deadline.strftime("%d.%m.%Y %H:%M")}\n\n'),
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
