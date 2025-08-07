import queue

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.init import conf

from .midlewares import UpdateLogger, AddUser


bot = Bot(token=conf.bot_token)
dp = Dispatcher()
scheduler = AsyncIOScheduler()
q = queue.Queue()