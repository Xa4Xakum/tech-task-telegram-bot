from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.types import Message, ContentType
from aiogram.fsm.context import FSMContext
from loguru import logger

from config.init import conf

from ..filters import ChatType, Role

r = Router()
r.message.filter(
    ChatType('private'),
    Role(conf.roles.manager)
)


@r.message(Command('start'))
async def start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer('Привет! Что будем делать сегодня?')
