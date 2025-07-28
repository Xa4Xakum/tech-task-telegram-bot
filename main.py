'''
Разработал @Xa4_Xakum - связаться в тг
Заказать на кворке - https://kwork.ru/user/xakum
'''
from vkbottle.bot import Message
from vkbottle import API
from loguru import logger

from groupbot.init import bot
from groupbot import handlers
# /check https://m.vk.com/wall550211701_198?from=profile
# Групповой токен для запуска бота
# Юзерский токен с правами wall (твой "вечный")


# async def has_reposted(user_id: int, post_url: str) -> bool:
#     match = re.search(r"wall(-?\d+)_(\d+)", post_url)
#     correct = False
#     if not match:
#         raise ValueError("Неверный формат ссылки на пост")

#     post_data = post_url.split('https://m.vk.com/wall')[1].split('?')[0].split('_')
#     user_id = int(post_data[0])
#     post_id = int(post_data[1])

#     try:
#         # Берём последние 20 постов
#         response = await user_api.wall.get(owner_id=user_id, count=20)
#     except Exception as e:
#         raise RuntimeError(f"Не удалось получить стену пользователя: {e}")

#     linked_post = None
#     for post in response.items:
#         # Если у поста есть copy_history — значит это репост
#         if post.id == post_id:
#             linked_post = post
#     logger.info(f'нужный пост - {linked_post}')
#     history = linked_post.copy_history[0]
#     if history.owner_id == ORIGINAL_OWNER_ID and history.id == POST_ID: correct = True
#     return correct


def main():
    logger.info('Бот успешно запущен!')
    bot.run_forever()


if __name__ == '__main__':
    main()
