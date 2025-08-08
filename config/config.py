import os
from typing import Any, List

from dotenv import load_dotenv


class Roles():
    constructor = 'Конструктор'
    manager = 'Менеджер'


class TaskStatuses():
    open = 'Открыт'
    close = 'Закрыт'


class Config():
    '''Настройки бота'''

    def __init__(self, env_path: str) -> None:
        self.env_path = env_path
        self.roles = Roles()
        self.task_statuses = TaskStatuses()
        load_dotenv(env_path)

    def _get_from_env(self, key: str, to_int: bool = False) -> Any:
        '''Получить данные из env по ключу'''
        data = os.getenv(key=key)
        if data is None:
            raise ValueError(f'В {self.env_path} не указан {key}!')

        if to_int:
            data = self._to_int(data)
            if data is None:
                raise ValueError(f'{key} не является числом!')

        return data

    def _to_int(self, data) -> int | None:
        '''Перевод текстовых данных в числовые'''
        try: return int(data)
        except: return

    @property
    def bot_token(self) -> str:
        '''Токен бота'''
        return self._get_from_env('BOT_TOKEN')

    @property
    def admins(self) -> List[int]:
        '''ID админов'''
        alist = self._get_from_env('ADMINS').split(',')
        alist = [int(i) for i in alist]
        if len(alist) == 0:
            raise ValueError('Список адмнистраторов ADMINS пуст!')
        return alist

    @property
    def datetime_format(self) -> str:
        return "%d.%m.%Y %H:%M"

    @property
    def db_conneciton(self) -> str:
        '''Подключение к бд'''
        return 'sqlite:///database/Xakum.db'
