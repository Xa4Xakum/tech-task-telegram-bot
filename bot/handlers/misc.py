from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext
from loguru import logger

from config.init import conf

from ..filters import ChatType, Role

r = Router()
r.message.filter(ChatType('private'))


@r.message(Command('id'))
async def id(msg: Message):
    await msg.answer(f'Ваш id: <code>{msg.from_user.id}</code>', parse_mode='html')


@r.message(Command('start'), Role(None))
async def start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer('Привет! Не могу найти тебя в своей базе данных, обратись к менеджеру, чтобы тебя добавили')
