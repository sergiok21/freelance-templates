from aiogram import types

from shared.common.configs.bot import models
from shared.constructor.base import BaseNavigation, Constructor
from shared.database.models import Admin
from shared.utils.localization import ADMIN


class StartBuilder(BaseNavigation):
    def __init__(self, button_column=1):
        super().__init__(Admin)

        self.button_column = button_column

    def build(
            self,
            message: types.Message,
            message_id: int,
            text: str
    ):
        params = [
            {'callback_data': 'create_token', 'text': ADMIN.CREATE_TOKEN},
            {'callback_data': 'show_users:5', 'text': ADMIN.SHOW_USERS},
        ]
        reply_markup = Constructor.reply_markup(params=params, columns=self.button_column)

        data = {
            'chat_id': message.chat.id,
            'text': text,
            'reply_markup': reply_markup
        }

        return data, params


class CreateTokenBuilder(BaseNavigation):
    def __init__(self, button_column=1):
        super().__init__(Admin)

        self.button_column = button_column

    def build(
            self,
            message: types.Message,
            message_id: int,
            text: str
    ):
        params = [
            {'callback_data': '1', 'text': '1 месяц'},
            {'callback_data': '3', 'text': '3 месяц'},
            {'callback_data': '6', 'text': '6 месяцев'},
            {'callback_data': '12', 'text': '12 месяцев'},
            {'callback_data': 'admin_main_menu', 'text': 'Отмена'},
        ]

        reply_markup = Constructor.reply_markup(params=params, columns=self.button_column)

        data = {
            'chat_id': message.chat.id,
            'message_id': message_id,
            'text': text,
            'reply_markup': reply_markup,
        }

        return data, params


class SetTokenDateBuilder(BaseNavigation):
    def __init__(self, button_column=1):
        super().__init__(Admin)

        self.button_column = button_column

    def build(
            self,
            message: types.Message,
            message_id: int,
            text: str
    ):
        params = [
            {'callback_data': 'create_token', 'text': ADMIN.BACK_PAGE},
            {'callback_data': 'admin_main_menu', 'text': ADMIN.TO_HOME_PAGE},
        ]

        reply_markup = Constructor.reply_markup(params=params, columns=self.button_column)

        data = {
            'chat_id': message.chat.id,
            'message_id': message.message_id,
            'text': text,
            'reply_markup': reply_markup
        }

        return data, params


class UsersViewBuilder(BaseNavigation):
    def __init__(self, button_column=1):
        super().__init__(Admin)

        self.button_column = button_column

    def build(
            self,
            message: types.Message,
            message_id: int,
            text: str,
            from_: int,
            to_: int,
            users_id: list
    ):
        params = []

        if from_:
            params.append({'callback_data': f'show_users:{from_}', 'text': ADMIN.PREVIOUS})

        if len(users_id) == 6:
            params.append({'callback_data': f'show_users:{to_ + 5}', 'text': ADMIN.NEXT})

        params.append({'callback_data': 'admin_main_menu', 'text': ADMIN.BACK_PAGE})

        if len(params) > 2:
            self.button_column += 1

        reply_markup = Constructor.reply_markup(params=params, columns=self.button_column)

        data = {
            'chat_id': message.chat.id,
            'message_id': message_id,
            'text': text,
            'reply_markup': reply_markup
        }

        return data, params
