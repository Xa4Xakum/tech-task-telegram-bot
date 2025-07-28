from typing import List

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from .buttons import Buttons


class BaseKeyboard():
    '''Базовые клавиатуры'''

    btn = Buttons()


    def reply_markup_from_buttons(self, *btns: KeyboardButton, adjust: List[int] = [1]) -> ReplyKeyboardMarkup | None:
        '''Клава из реплай кнопок, если они есть'''
        if len(btns) == 0:
            return

        builder = ReplyKeyboardBuilder()
        builder.add(*btns)
        builder.adjust(*adjust)
        return builder.as_markup(resize_keyboard=True)


    def inline_markup_from_buttons(self, *btns: InlineKeyboardButton, adjust: List[int] = [1]) -> InlineKeyboardMarkup | None:
        '''Клава из инлайн кнопок, если они есть'''
        if len(btns) == 0:
            return

        builder = InlineKeyboardBuilder()
        builder.add(*btns)
        builder.adjust(*adjust)
        return builder.as_markup()


class UserKeyboards(BaseKeyboard):
    '''Клавиатуры пользователей'''


class ManagerKeyboards(BaseKeyboard):
    '''Клавиатуры админов''' 

    @property
    def menu(self):
        return self.reply_markup_from_buttons(
            self.btn.manager.create_task,
            self.btn.manager.show_answers,
        )


class Keyboards(BaseKeyboard):
    '''Все клавиатуры бота(включая общие)'''

    btn = Buttons()
    user = UserKeyboards()
    manager = ManagerKeyboards()
