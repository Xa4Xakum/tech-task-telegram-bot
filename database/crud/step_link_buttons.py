from typing import List

from ..base import BaseCrud
from ..models import StepLinksButtons


class Add(BaseCrud):
    '''Методы добавления'''

    def add(
        self,
        step_id: int,
        url: str,
        btn_text: str,
    ) -> None:
        '''
        Добавление записи о шаге

        :param step_id: Айди шага
        :param url: Подарочная ссылка для кнопки
        :param btn_text: Текст кнопки-ссылки
        '''
        with self.session() as s:
            step = StepLinksButtons(
                step_id=step_id,
                url=url,
                btn_text=btn_text
            )
            s.add(step)
            s.commit()


class Update(BaseCrud):
    '''Методы изменения'''


    def update_text(
        self,
        step_id: int,
        text: str
    ) -> None:
        '''
        Изменение текста кнопки

        :param step_id: id шага
        :param url: url кнопки
        :param text: новый text кнопки
        '''
        with self.session() as s:
            s.query(StepLinksButtons).filter(
                StepLinksButtons.step_id == step_id,
            ).update({
                StepLinksButtons.btn_text: text
            })
            s.commit()


    def update_url(
        self,
        step_id: int,
        url: str,
    ) -> None:
        '''
        Изменение ссылки кнопки

        :param step_id: id шага
        :param url: url кнопки
        '''
        with self.session() as s:
            filter = (
                StepLinksButtons.step_id == step_id,
                StepLinksButtons.url == url,
            )

            old_btn = s.query(
                StepLinksButtons
            ).filter(
                *filter
            ).first()

            new_btn = StepLinksButtons(
                step_id=step_id,
                url=url,
                text=old_btn.btn_text if old_btn else 'текста нет'
            )

            s.add(new_btn)
            s.commit()


class Get(BaseCrud):
    '''Методы получения'''

    def get_by_step_id(
        self,
        step_id: int,
    ) -> List[StepLinksButtons]:
        '''
        Получение подарочных кнопок шага

        :param step_id: id шага
        '''
        with self.session() as s:
            return s.query(StepLinksButtons).filter(
                StepLinksButtons.step_id == step_id
            ).first()


class CRUD(Add, Update, Get):
    '''Класс с методами добавления, получения, изменения и удаления'''
