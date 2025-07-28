from aiogram.types import KeyboardButton



class UserButtons():
    '''Кнопки пользователей'''


class ManagerButtons():
    '''Кнопки менеджеров'''

    create_task = KeyboardButton(text='Создать ТЗ')
    opened_tasks = KeyboardButton(text='Открытые ТЗ')
    show_answers = KeyboardButton(text='Посмотреть ответы')


class Buttons():
    '''Все кнопки бота (включая общие)'''

    user = UserButtons()
    manager = ManagerButtons()
