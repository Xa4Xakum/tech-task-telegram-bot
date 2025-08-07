from ..base import BaseCrud
from ..models import Media


class Add(BaseCrud):
    '''Методы добавления медиафайлов'''

    def add(self, task_id: int, file_id: int, media_type: str) -> None:
        with self.session() as s:
            entry = Media(
                task_id=task_id,
                file_id=file_id,
                media_type=media_type
            )
            s.add(entry)
            s.commit()


class Del(BaseCrud):
    '''Методы удаления медиафайлов'''

    def del_by_task(self, task_id: int) -> None:
        with self.session() as s:
            s.query(Media).filter(
                Media.task_id == task_id
            ).delete()
            s.commit()


class CRUD(Add, Del):
    '''CRUD для медиафайлов'''
