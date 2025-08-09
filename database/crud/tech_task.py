from typing import List
from datetime import datetime

from sqlalchemy import desc

from ..base import BaseCrud
from ..models import TechTask, Answer


class Add(BaseCrud):
    '''Методы добавления технических заданий'''

    def add(
        self,
        text: str,
        owner_id: int,
        deadline: datetime,
        status: str,
    ) -> TechTask:
        with self.session() as s:
            entry = TechTask(
                text=text,
                owner_id=owner_id,
                deadline=deadline,
                status=status
            )
            s.add(entry)
            s.commit()
            s.refresh(entry)
            return entry


class Get(BaseCrud):
    '''Методы получения технических заданий'''

    def get_by_id(self, id: int) -> TechTask | None:
        with self.session() as s:
            return s.query(TechTask).filter(
                TechTask.id == id
            ).first()

    def get_first_not_answered(
        self,
        user_id: int,
        offset: int = 0,
    ) -> TechTask | None:
        '''Получить все ТЗ, на которые пользователь ещё не ответил'''
        with self.session() as s:
            subq = s.query(Answer.task_id).filter(Answer.user_id == user_id).subquery()
            query = s.query(
                TechTask
            ).filter(
                ~TechTask.id.in_(subq)
            ).order_by(
                TechTask.id
            ).offset(
                offset
            )
            return query.first()

    def get_all(self) -> List[TechTask]:
        with self.session() as s:
            return s.query(
                TechTask
            ).order_by(
                desc(TechTask.update_at)
            ).all()

    def get_not_my(self, owner_id: int) -> List[TechTask]:
        with self.session() as s:
            return s.query(
                TechTask
            ).filter(
                TechTask.owner_id != owner_id
            ).order_by(
                desc(TechTask.update_at)
            ).all()

    def get_my(self, owner_id: int) -> List[TechTask]:
        with self.session() as s:
            return s.query(
                TechTask
            ).filter(
                TechTask.owner_id == owner_id
            ).order_by(
                desc(TechTask.update_at)
            ).all()

    def get_with_deadline_smaller_than(self, deadline: datetime) -> List[TechTask]:
        with self.session() as s:
            return s.query(
                TechTask
            ).filter(
                TechTask.deadline < deadline,
                TechTask.deadline > datetime.now()
            ).all()

    def get_opened(self) -> List[TechTask]:
        with self.session() as s:
            return s.query(
                TechTask
            ).filter(
                TechTask.deadline > datetime.now()
            ).all()
    

class Update(BaseCrud):
    '''Методы изменения технических заданий'''

    def update_status(self, id: int, status: str) -> None:
        with self.session() as s:
            s.query(TechTask).filter(
                TechTask.id == id
            ).update({
                TechTask.status: status,
            })
            s.commit()

    def update_deadline(self, task_id: int, deadline: datetime) -> None:
        with self.session() as s:
            s.query(TechTask).filter(
                TechTask.id == task_id,
            ).update({
                TechTask.deadline: deadline,
            })
            s.commit()

    def update_text(self, task_id: int, text: str) -> None:
        with self.session() as s:
            s.query(TechTask).filter(
                TechTask.id == task_id,
            ).update({
                TechTask.text: text,
            })
            s.commit()

class Del(BaseCrud):
    '''Методы удаления технических заданий'''

    def del_by_id(self, id: int) -> None:
        with self.session() as s:
            s.query(TechTask).filter(
                TechTask.id == id
            ).delete()
            s.commit()


class CRUD(Add, Get, Update, Del):
    '''CRUD для технических заданий'''
