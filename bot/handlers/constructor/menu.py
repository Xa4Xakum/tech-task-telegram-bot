from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from loguru import logger

from config.init import conf
from utils.misc import try_to_int
from database.init import db

from ...keyboards import kb
from ...filters import ChatType, Role
from ...states import ConstructorStates

r = Router()
r.message.filter(
    ChatType('private'),
    Role(conf.roles.constructor)
)


@r.message(Command('start'))
@r.message(F.text == kb.btn.to_menu.text, StateFilter('*'))
async def start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer('Выберите действие:', reply_markup=kb.constructor.menu)


@r.message(F.text == kb.btn.constructor.opened_tasks.text)
async def opened_task(msg: Message):
    await msg.answer('В разработке...')
