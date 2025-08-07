from datetime import datetime
from typing import List

from ..base import BaseCrud
from ..models import Answer


class Add(BaseCrud):
    '''Методы добавления ответов на ТЗ'''

    def add(
        self,
        task_id: int,
        user_id: int,
        text: str,
        price: int,
        deadline: datetime,
    ) -> None:
        with self.session() as s:
            entry = Answer(
                task_id=task_id,
                user_id=user_id,
                text=text,
                price=price,
                deadline=deadline
            )
            s.add(entry)
            s.commit()
            s.refresh(entry)


class Get(BaseCrud):
    '''Методы получения ответов'''

    def get_by_task(self, task_id: int) -> List[Answer]:
        with self.session() as s:
            return s.query(Answer).filter(
                Answer.task_id == task_id
            ).all()


    def get_by_ids(self, task_id: int, user_id: int) -> Answer | None:
        with self.session() as s:
            return s.query(Answer).filter(
                Answer.task_id == task_id,
                Answer.user_id == user_id
            ).first()


class Del(BaseCrud):
    '''Методы удаления ответов'''

    def del_by_user(self, task_id: int, user_id: int) -> None:
        with self.session() as s:
            s.query(Answer).filter(
                Answer.task_id == task_id,
                Answer.user_id == user_id
            ).delete()
            s.commit()


class CRUD(Add, Get, Del):
    '''CRUD для ответов на ТЗ'''
