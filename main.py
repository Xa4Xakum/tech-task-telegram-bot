'''
Разработал @Xa4_Xakum - связаться в тг
Заказать на кворке - https://kwork.ru/user/xakum
'''

import asyncio

from loguru import logger

from bot.midlewares import AddUser, UpdateLogger
from bot.init import dp, bot, q, scheduler
from bot.misc import deadline_notify


async def on_startup():
    bot_info = await bot.get_me()
    scheduler.add_job(deadline_notify, "interval", minutes=10, misfire_grace_time=599)
    scheduler.start()
    logger.info(f'Бот {bot_info.username} успешно запущен!')


def include_constructor_routers():
    from bot.handlers.constructor import menu, answer, task_history
    dp.include_routers(
        menu.r,
        answer.r,
        task_history.r
    )


def include_manager_routers():
    from bot.handlers.manager import menu, create_task, task_history, task_answers
    dp.include_routers(
        menu.r,
        create_task.r,
        task_history.r,
        task_answers.r
    )


def include_routers():
    from bot.handlers import admin, misc
    dp.include_routers(
        admin.r,
        misc.r,
    )
    include_constructor_routers()
    include_manager_routers()


async def main():
    dp.update.outer_middleware(AddUser())
    dp.update.middleware(UpdateLogger())
    logger.info('Мидлвари подключены')
    dp.startup.register(on_startup)
    include_routers()
    logger.info('Роутеры подключены')
    asyncio.create_task(queue_process())
    logger.info('Обработка очереди запущена')
    await dp.start_polling(bot)


async def queue_process():
    while True:
        while not q.empty():
            logger.info(f'Выполнение задачи из очереди')
            await q.get()  # очередь должна хранить в себе готовые корутины - только заавеитить их и все
        logger.info('задачи кончились')
        await asyncio.sleep(10)


if __name__ == '__main__':
    asyncio.run(main())
