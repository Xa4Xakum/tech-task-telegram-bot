from typing import List

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from .buttons import Buttons


class BaseKeyboard():
    '''Базовые клавиатуры'''

    btn = Buttons()


    def reply_markup_from_buttons(self, *btns: KeyboardButton, adjust: List[int] | None = None) -> ReplyKeyboardMarkup | None:
        '''Клава из реплай кнопок, если они есть'''
        if len(btns) == 0:
            return

        if not adjust: adjust = [1]
        builder = ReplyKeyboardBuilder()
        builder.add(*btns)
        builder.adjust(*adjust)
        return builder.as_markup(resize_keyboard=True)


    def inline_markup_from_buttons(self, *btns: InlineKeyboardButton, adjust: List[int] | None = None) -> InlineKeyboardMarkup | None:
        '''Клава из инлайн кнопок, если они есть'''
        if len(btns) == 0:
            return

        if not adjust: adjust = [1]
        builder = InlineKeyboardBuilder()
        builder.add(*btns)
        builder.adjust(*adjust)
        return builder.as_markup()


class ManagerKeyboards(BaseKeyboard):
    '''Клавиатуры админов''' 

    @property
    def menu(self):
        return self.reply_markup_from_buttons(
            self.btn.manager.create_task,
            self.btn.manager.opened_tasks,
            self.btn.manager.tasks_history,
        )

    @property
    def choose_tasks_owner(self):
        return self.reply_markup_from_buttons(
            self.btn.manager.my_tasks,
            self.btn.manager.other_tasks,
            self.btn.to_menu,
            adjust=[2,1]
        )

    @property
    def corusel_with_show_answers(self):
        return self.reply_markup_from_buttons(
            self.btn.previous,
            self.btn.manager.show_answers,
            self.btn.next,
            self.btn.to_menu,
            adjust=[3,1]
        )

    @property
    def corusel_with_show_answers_and_edit(self):
        return self.reply_markup_from_buttons(
            self.btn.previous,
            self.btn.manager.show_answers,
            self.btn.next,
            self.btn.edit,
            self.btn.to_menu,
            adjust=[3,1,1]
        )

    @property
    def corusel_with_edit(self):
        return self.reply_markup_from_buttons(
            self.btn.previous,
            self.btn.edit,
            self.btn.next,
            self.btn.to_menu,
            adjust=[3,1]
        )

    @property
    def corusel_with_back_to_tasks(self):
        return self.reply_markup_from_buttons(
            self.btn.previous,
            self.btn.to_history,
            self.btn.next,
            self.btn.to_menu,
            adjust=[3,1]
        )

    @property
    def edit_task(self):
        return self.reply_markup_from_buttons(
            self.btn.deadline,
            self.btn.manager.text,
            self.btn.manager.attachments,
            self.btn.to_history,
            self.btn.to_menu,
            adjust=[3,1,1]
        )

    @property
    def edit_attachments(self):
        return self.reply_markup_from_buttons(
            self.btn.ready,
            self.btn.manager.del_attachments,
            self.btn.to_history,
            self.btn.to_menu,
            adjust=[2,1,1]
        )


class ConstructorKeyboards(BaseKeyboard):
    '''Клавиатуры конструкторов'''

    @property
    def menu(self):
        return self.reply_markup_from_buttons(
            self.btn.constructor.opened_tasks,
            self.btn.constructor.tasks_history,
        )

    @property
    def corusel_with_answer(self):
        return self.reply_markup_from_buttons(
            self.btn.previous,
            self.btn.constructor.answer_reply,
            self.btn.next,
            self.btn.to_menu,
            adjust=[3,1]
        )

    @property
    def corusel_with_show_answer(self):
        return self.reply_markup_from_buttons(
            self.btn.previous,
            self.btn.constructor.show_answer,
            self.btn.next,
            self.btn.to_menu,
            adjust=[3,1]
        )

    @property
    def edit_answer(self):
        return self.reply_markup_from_buttons(
            self.btn.deadline,
            self.btn.price,
            self.btn.constructor.comment,
            self.btn.to_history,
            adjust=[3,1]
        )

    @property
    def without_com(self):
        return self.reply_markup_from_buttons(
            self.btn.constructor.without_com,
        )

    def answer(self, task_id: int):
        return self.inline_markup_from_buttons(
            InlineKeyboardButton(
                text=self.btn.constructor.answer.text,
                callback_data=f"{self.btn.constructor.answer.callback_data}:{task_id}",
            )
        )


class Keyboards(BaseKeyboard):
    '''Все клавиатуры бота(включая общие)'''

    btn = Buttons()
    constructor = ConstructorKeyboards()
    manager = ManagerKeyboards()

    @property
    def check(self):
        return self.reply_markup_from_buttons(
            self.btn.all_good,
            self.btn.cancel
        )

    @property
    def after_edit(self):
        return self.reply_markup_from_buttons(
            self.btn.continue_edit,
            self.btn.to_history,
        )

    @property
    def cancel(self):
        return self.reply_markup_from_buttons(
            self.btn.cancel
        )


    @property
    def ready(self):
        return self.reply_markup_from_buttons(
            self.btn.ready,
            self.btn.skip,
            self.btn.cancel
        )

    @property
    def to_menu(self):
        return self.reply_markup_from_buttons(
            self.btn.to_menu,
        )

    @property
    def corusel(self):
        return self.reply_markup_from_buttons(
            self.btn.previous,
            self.btn.next,
            self.btn.to_menu,
            adjust=[2,1]
        )

    @property
    def corusel_with_edit(self):
        return self.reply_markup_from_buttons(
            self.btn.previous,
            self.btn.edit,
            self.btn.next,
            self.btn.to_menu,
            adjust=[3,1]
        )


kb = Keyboards()
