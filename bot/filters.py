from typing import Optional, List

from aiogram.filters import BaseFilter
from aiogram.types import Message

from database.init import db
from config.init import conf


class ChatType(BaseFilter):
    def __init__(self, *chat_types: str):
        self.chat_types = chat_types

    async def __call__(self, message: Message) -> bool:
        return message.chat.type in self.chat_types


class ChatsId(BaseFilter):
    def __init__(self, *chats: int):
        self.chats = chats

    async def __call__(self, message: Message) -> bool:
        return message.chat.id in self.chats


class Role(BaseFilter):
    def __init__(self, *roles: str | None) -> None:
        self.roles = roles

    async def __call__(self, msg: Message) -> bool:
        user = db.user.get_by_id(msg.from_user.id)
        if not user: return False
        return user.role in self.roles


class FromId(BaseFilter):
    def __init__(self, *user_id: int) -> None:
        self.user_ids = user_id

    async def __call__(self, msg: Message) -> bool:
        return msg.from_user.id in self.user_ids
