from datetime import datetime
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer, String, ForeignKey, DateTime
)

from .base import Base


class Media(Base):
    __tablename__ = 'task_media'

    task_id: Mapped[int] = mapped_column(Integer, ForeignKey('tech_tasks.id', ondelete='CASCADE'), primary_key=True)
    file_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    media_type: Mapped[str] = mapped_column(String)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[str] = mapped_column(String, nullable=True, default=None)
    username: Mapped[str] = mapped_column(String, nullable=True)


class TechTask(Base):
    __tablename__ = 'tech_tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    text: Mapped[str] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    deadline: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    update_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now)

    media: Mapped[List['Media']] = relationship(
        'Media',
        lazy='selectin',
        cascade='all, delete-orphan',
        passive_deletes=True
    )


class Answer(Base):
    __tablename__ = 'answer'

    task_id: Mapped[int] = mapped_column(Integer, ForeignKey('tech_tasks.id', ondelete='CASCADE'), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    text: Mapped[str] = mapped_column(String)
    price: Mapped[str] = mapped_column(String)  # Попросили в цену добавлять еще и буквы, штош, пусть так
    deadline: Mapped[datetime] = mapped_column(DateTime)
