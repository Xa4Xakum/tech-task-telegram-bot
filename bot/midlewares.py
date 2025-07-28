from datetime import datetime
from typing import Callable, Dict, Any, Awaitable
from time import perf_counter

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from aiogram.fsm.context import FSMContext
from aiogram.dispatcher.flags import get_flag
from loguru import logger

from database.init import db


class AddUser(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        shortcut = event.message if event.message else event.callback_query
        user_id = shortcut.from_user.id
        user = db.user.get_by_id(user_id)
        if not user: db.user.add(user_id, shortcut.from_user.username)
        return await handler(event, data)


class UpdateLogger(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        start_time = perf_counter()
        if event.message:
            msg_content_type = event.message.content_type
            event_type = f'сообщение({msg_content_type})'
            event_text = event.message.caption if msg_content_type == 'photo' else event.message.text
        elif event.callback_query:
            event_type = 'колбек'
            event_text = event.callback_query.data
        else:
            event_type = 'неизвестный'
            event_text = 'неизвестный'
        state = data['state']
        logger.info(
            f'Пришел апдейт типа {event_type} от @{data["event_from_user"].username} '
            f'с текстом {event_text}, state = {await state.get_state()}'
        )
        result = await handler(event, data)

        end_time = perf_counter()
        logger.info(f'Апдейт от @{data["event_from_user"].username} обработан за {round(end_time - start_time, 3)} секунд')
        return result
