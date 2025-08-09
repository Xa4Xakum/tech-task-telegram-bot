from aiogram.types import KeyboardButton, InlineKeyboardButton



class ManagerButtons():
    '''Кнопки менеджеров'''

    create_task = KeyboardButton(text='Создать ТЗ')
    opened_tasks = KeyboardButton(text='Открытые ТЗ')
    tasks_history = KeyboardButton(text='История ТЗ')
    show_answers = KeyboardButton(text='Ответы')
    back_to_tasks = KeyboardButton(text='Назад к ТЗ')
    my_tasks = KeyboardButton(text='Мои ТЗ')
    other_tasks = KeyboardButton(text='Другие ТЗ')
    text = KeyboardButton(text="Текст ТЗ")
    attachments = KeyboardButton(text='Вложения')
    del_attachments = KeyboardButton(text='Удалить текущие')


class ConstructorButtons():
    '''Кнопки конструкторов'''

    opened_tasks = KeyboardButton(text='Открытые ТЗ')
    tasks_history = KeyboardButton(text='История ТЗ')
    answer = InlineKeyboardButton(text='Ответить', callback_data='answer')
    answer_reply = KeyboardButton(text='Ответить')
    show_answer = KeyboardButton(text='Мой ответ')
    without_com = KeyboardButton(text='Без комментария')
    comment = KeyboardButton(text='Комментарий')

    give_assessment = KeyboardButton(text='Дать оценку')
    ask_question = KeyboardButton(text='Задать вопрос')


class Buttons():
    '''Все кнопки бота (включая общие)'''

    constructor = ConstructorButtons()
    manager = ManagerButtons()

    cancel = KeyboardButton(text='Отмена')
    all_good = KeyboardButton(text='Все верно')
    ready = KeyboardButton(text='Готово')
    skip = KeyboardButton(text='Пропустить')
    to_menu = KeyboardButton(text='В меню')
    edit = KeyboardButton(text='Изменить')
    continue_edit = KeyboardButton(text='Продолжить изменение')
    to_history = KeyboardButton(text='К истории ТЗ')

    deadline = KeyboardButton(text='Дедлайн')
    price = KeyboardButton(text='Цену')

    next = KeyboardButton(text='Дальше')
    previous = KeyboardButton(text='Назад')
