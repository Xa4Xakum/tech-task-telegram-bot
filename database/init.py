from .crud import user

from .base import Base, engine, SessionFactory


class DataBase():
    '''
    Класс для работы с базой данных
    '''

    def __init__(self) -> None:
        Base.metadata.create_all(engine, checkfirst=True)
        self.user = user.CRUD(SessionFactory)


db = DataBase()
