from abc import ABC, abstractmethod
from typing import Type

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from shared.database.models import User, Admin


class Constructor:
    @staticmethod
    def reply_markup(params: list, columns) -> InlineKeyboardMarkup:
        keyboard = []
        sub_buttons = []
        for param in params:
            sub_buttons.append(InlineKeyboardButton(**param))
            if len(sub_buttons) == columns:
                keyboard.append(sub_buttons)
                sub_buttons = []
        keyboard.append(sub_buttons) if sub_buttons else keyboard
        return InlineKeyboardMarkup(inline_keyboard=keyboard)


class BaseNavigation(ABC):
    def __init__(self, model: Type[User | Admin]):
        self.model = model

    @abstractmethod
    def build(self, **kwargs):
        pass
