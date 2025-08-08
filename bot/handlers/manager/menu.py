from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

from config.init import conf

from ...keyboards import kb
from ...filters import ChatType, Role
from ...states import CreateTaskStates

r = Router()
r.message.filter(
    ChatType('private'),
    Role(conf.roles.manager)
)


@r.message(F.text==kb.btn.cancel.text, StateFilter(CreateTaskStates))
@r.message(F.text==kb.btn.to_menu.text)
@r.message(Command('start'))
async def start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer('Выберите действие:', reply_markup=kb.manager.menu)


@r.message(F.text == kb.btn.manager.opened_tasks.text)
async def opened_task(msg: Message):
    await msg.answer('В разработке...')
