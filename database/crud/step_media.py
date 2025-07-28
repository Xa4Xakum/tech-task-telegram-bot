from typing import List

from ..base import BaseCrud
from ..models import StepMedia


class Add(BaseCrud):
    '''Методы добавления шагов'''

    def add(
        self,
        step_id: int,
        media_id: int,
        owner_id: int,
        media_type: str
    ) -> None:
        '''
        Добавление медиа-вложения к шагу
        '''
        with self.session() as s:
            step_media = StepMedia(
                step_id=step_id,
                media_id=media_id,
                owner_id=owner_id,
                media_type=media_type,
            )
            s.add(step_media)
            s.commit()


class Get(BaseCrud):
    '''Методы получения шагов'''

    def get_by_step_id(
        self,
        step_id: int,
    ) -> List[StepMedia]:
        '''
        Получение медиа-вложений шага
        '''
        with self.session() as s:
            return s.query(StepMedia).filter(
                StepMedia.step_id == step_id
            ).all()


class Delete(BaseCrud):
    '''Методы удаления медиа'''

    def delete_by_step_id(self, step_id: int) -> None:
        '''
        Удаление всех медиа-вложений у конкретного шага
        '''
        with self.session() as s:
            s.query(StepMedia).filter(StepMedia.step_id == step_id).delete()
            s.commit()


class CRUD(Add, Get, Delete):
    '''Класс с методами добавления, получения, изменения и удаления'''
