from typing import List

from ..base import BaseCrud
from ..models import User


class Add(BaseCrud):
    '''Методы добавления'''

    def add(
        self,
        id: int,
        username: str | None = None,
        role: str | None = None,
    ) -> None:
        with self.session() as s:
            entry = User(
                id=id,
                username=username,
                role=role,
            )
            s.add(entry)
            s.commit()


class Get(BaseCrud):
    '''Методы получения'''


    def get_by_id(
        self,
        id: int,
    ) -> User | None:
        with self.session() as s:
            return s.query(User).filter(
                User.id == id
            ).first()


    def get_all_with_role(
        self,
        role: str,
    ) -> List[User]:
        with self.session() as s:
            return s.query(User).filter(
                User.role == role
            ).all()


    def get_all(self) -> List[User]:
        with self.session() as s:
            return s.query(
                User
            ).all()


class Update(BaseCrud):
    '''Методы изменения'''


    def update_role(
        self,
        id: int,
        role: str | None = None,
    ) -> None:
        with self.session() as s:
            s.query(User).filter(
                User.id == id
            ).update({
                User.role: role
            })
            s.commit()


class Del(BaseCrud):
    '''Методы получения шагов'''

    def del_by_id(
        self,
        id: int,
    ) -> None:
        with self.session() as s:
            s.query(User).filter(
                User.id == id
            ).delete()
            s.commit()


class CRUD(Add, Get, Update, Del):
    '''Класс с методами добавления, получения, изменения и удаления'''
