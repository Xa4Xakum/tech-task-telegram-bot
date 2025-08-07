from .crud import user, tech_task, media, answer

from .base import Base, engine, SessionFactory


class DataBase():
    '''
    Класс для работы с базой данных
    '''

    def __init__(self) -> None:
        Base.metadata.create_all(engine, checkfirst=True)
        self.user = user.CRUD(SessionFactory)
        self.tech_task = tech_task.CRUD(SessionFactory)
        self.media = media.CRUD(SessionFactory)
        self.answer = answer.CRUD(SessionFactory)


db = DataBase()
