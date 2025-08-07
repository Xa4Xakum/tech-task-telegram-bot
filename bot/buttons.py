from aiogram.types import KeyboardButton, InlineKeyboardButton



class ManagerButtons():
    '''Кнопки менеджеров'''

    create_task = KeyboardButton(text='Создать ТЗ')
    opened_tasks = KeyboardButton(text='Открытые ТЗ')
    tasks_history = KeyboardButton(text='История ТЗ')


class ConstructorButtons():
    '''Кнопки конструкторов'''

    opened_tasks = KeyboardButton(text='Открытые ТЗ')
    tasks_history = KeyboardButton(text='История ТЗ')
    answer = InlineKeyboardButton(text='Ответить', callback_data='answer')
    answer_reply = KeyboardButton(text='Ответить')
    show_answer = KeyboardButton(text='Мой ответ')
    without_com = KeyboardButton(text='Без комментария')


class Buttons():
    '''Все кнопки бота (включая общие)'''

    constructor = ConstructorButtons()
    manager = ManagerButtons()

    cancel = KeyboardButton(text='Отмена')
    all_good = KeyboardButton(text='Все верно')
    ready = KeyboardButton(text='Готово')
    skip = KeyboardButton(text='Пропустить')
    to_menu = KeyboardButton(text='В меню')

    next = KeyboardButton(text='Дальше')
    previous = KeyboardButton(text='Назад')
