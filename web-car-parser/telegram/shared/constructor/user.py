import os

from aiogram import types
from aiogram.types import WebAppInfo

from shared.common.configs.urls import Support
from shared.constructor.base import BaseNavigation, Constructor
from shared.database.models import User
from shared.utils.localization import BaseLanguage, LanguageProcessor


class StartBuilder(BaseNavigation):
    def __init__(self, button_column=1):
        super().__init__(User)

        self.button_column = button_column

    def build(
            self,
            message: types.Message,
            message_id: int,
            text: str
    ):
        params = [
            {'callback_data': 'activate_account:eng', 'text': 'English'},
            {'callback_data': 'activate_account:slo', 'text': 'Slovenski'},
            {'callback_data': 'activate_account:ru', 'text': 'Russian'}
        ]
        reply_markup = Constructor.reply_markup(params=params, columns=self.button_column)

        data = {
            'chat_id': message.chat.id,
            'text': text,
            'reply_markup': reply_markup
        }

        return data, params


class ActivateAccountBuilder(BaseNavigation):
    def __init__(self, button_column=1):
        super().__init__(User)

        self.button_column = button_column

    def build(
            self,
            message: types.Message,
            user_lang: BaseLanguage,
            message_id: int,
            text: str
    ):
        params = [
            {'callback_data': 'buy_subscription', 'text': user_lang.BUY_SUBSCRIPTION, 'url': Support.MANAGER}
        ]
        reply_markup = Constructor.reply_markup(params=params, columns=self.button_column)

        data = {
            'chat_id': message.chat.id,
            'message_id': message.message_id,
            'text': text,
            'reply_markup': reply_markup
        }

        return data, params

    def build_params(self, user_lang: BaseLanguage):
        params = [
            {'callback_data': 'buy_subscription', 'text': user_lang.BUY_SUBSCRIPTION, 'url': Support.MANAGER}
        ]
        return params


class MenuBuilder(BaseNavigation):
    def __init__(self, button_column=1):
        super().__init__(User)

        self.button_column = button_column

    def build(
            self,
            message: types.Message,
            message_id: int,
            user_lang: BaseLanguage,
            text: str
    ):
        params = [
            {'callback_data': 'bot_configuration', 'text': user_lang.BOT_SETTING_IN_MAIN_MENU},
            {'callback_data': 'profile_configuration', 'text': user_lang.PROFILE_SETTING_IN_MAIN_MENU},
            {'callback_data': 'support', 'text': user_lang.SUPPORT_IN_MAIN_MENU},
            {'callback_data': 'manual', 'text': user_lang.INSTRUCTION_IN_MAIN_MENU, 'url': user_lang.INSTRUCTION_URL},
        ]
        reply_markup = Constructor.reply_markup(params=params, columns=self.button_column)

        data = {
            'chat_id': message.chat.id,
            'message_id': message_id,
            'text': text,
            'reply_markup': reply_markup
        }

        return data, params


class ProfileConfigurationBuilder(BaseNavigation):
    def __init__(self, button_column=1):
        super().__init__(User)

        self.button_column = button_column

    def build(
            self,
            message: types.Message,
            message_id: int,
            user_lang: BaseLanguage,
            text: str
    ):
        params = [
            {'callback_data': 'subscriptions', 'text': user_lang.SUBSCRIPTIONS},
            {'callback_data': 'change_language', 'text': user_lang.CHANGE_LANGUAGE},
            {'callback_data': 'notices', 'text': user_lang.NOTICES},
            {'callback_data': 'main_menu', 'text': user_lang.BACK},
        ]
        reply_markup = Constructor.reply_markup(params=params, columns=self.button_column)

        data = {
            'chat_id': message.chat.id,
            'message_id': message.message_id,
            'text': user_lang.PROFILE_SETTINGS_SECTION,
            'reply_markup': reply_markup
        }

        return data, params


class SubscriptionBuilder(BaseNavigation):
    def __init__(self, button_column=1):
        super().__init__(User)

        self.button_column = button_column

    def build(
            self,
            message: types.Message,
            message_id: int,
            user_lang: BaseLanguage,
            text: str
    ):
        params = [
            {'callback_data': 'update_subscription', 'text': user_lang.UPDATE_SUBSCRIPTION},
            {'callback_data': 'profile_configuration', 'text': user_lang.BACK},
            {'callback_data': 'main_menu', 'text': user_lang.TO_HOME_PAGE},
        ]
        reply_markup = Constructor.reply_markup(params=params, columns=self.button_column)

        data = {
            'chat_id': message.chat.id,
            'message_id': message_id,
            'text': text,
            'reply_markup': reply_markup
        }

        return data, params


class UpdateSubscriptionBuilder(BaseNavigation):
    def __init__(self, button_column=1):
        super().__init__(User)

        self.button_column = button_column

    def build(
            self,
            message: types.Message,
            user_lang: BaseLanguage,
            message_id: int,
            text: str
    ):
        params = [
            {'callback_data': 'buy_subscription', 'text': user_lang.BUY_SUBSCRIPTION,
             'url': Support.MANAGER},
            {'callback_data': 'subscriptions', 'text': user_lang.BACK},
            {'callback_data': 'main_menu', 'text': user_lang.TO_HOME_PAGE},
        ]
        reply_markup = Constructor.reply_markup(params=params, columns=self.button_column)

        data = {
            'chat_id': message.chat.id,
            'message_id': message_id,
            'text': text,
            'reply_markup': reply_markup
        }

        return data, params


class NoticeBuilder(BaseNavigation):
    def __init__(self, button_column=1):
        super().__init__(User)

        self.button_column = button_column

    def build(
            self,
            message: types.Message,
            user_lang: BaseLanguage,
            message_id: int,
            payment: bool,
            text: str = None
    ):
        params = [
            {
                'callback_data': f'notices:payment:{payment}',
                'text': user_lang.PAYMENT_REMINDER_STATUS.format(user_lang.ON if payment else user_lang.OFF)
            },
            {'callback_data': 'profile_configuration', 'text': user_lang.BACK},
            {'callback_data': 'main_menu', 'text': user_lang.TO_HOME_PAGE},
        ]
        reply_markup = Constructor.reply_markup(params=params, columns=self.button_column)

        data = {
            'chat_id': message.chat.id,
            'message_id': message.message_id,
            'text': text,
            'reply_markup': reply_markup
        }

        if not text:
            del data['text']

        return data, params


class ChangeLanguageBuilder(BaseNavigation):
    def __init__(self, button_column=1):
        super().__init__(User)

        self.button_column = button_column

    def build(
            self,
            message: types.Message,
            user_lang: BaseLanguage,
            message_id: int,
            text: str
    ):
        languages = [
            {
                f'callback_data': f'change_language:{LanguageProcessor.CODES[i]}',
                'text': f'{LanguageProcessor.LANGUAGES[i]}'
            }
            for i in range(len(LanguageProcessor.LANGUAGES))
        ]
        params = [
            *languages,
            {'callback_data': 'profile_configuration', 'text': user_lang.BACK},
            {'callback_data': 'main_menu', 'text': user_lang.TO_HOME_PAGE},
        ]
        reply_markup = Constructor.reply_markup(params=params, columns=self.button_column)

        data = {
            'chat_id': message.chat.id,
            'message_id': message.message_id,
            'text': text,
            'reply_markup': reply_markup
        }

        return data, params


class BotBuilder(BaseNavigation):
    def __init__(self, button_column=1):
        super().__init__(User)

        self.button_column = button_column

    def build(
            self,
            message: types.Message,
            message_id: int,
            user_lang: BaseLanguage,
            status: bool,
            token: str,
            text: str = None,
    ):
        web_app = WebAppInfo(
            url=f'{os.environ.get("WEB_URL")}/{user_lang.REQUEST_CODE}/home?'
                f'user_id={message.chat.id}&token={token}&started={status}'
        )

        params = [
            {'callback_data': f'bot_status:{status}', 'text': user_lang.STOP_BOT if status else user_lang.START_BOT},
            {'text': user_lang.FILTERS, 'web_app': web_app},
            {'callback_data': 'main_menu', 'text': user_lang.BACK},
        ]
        reply_markup = Constructor.reply_markup(params=params, columns=self.button_column)

        data = {
            'chat_id': message.chat.id,
            'message_id': message.message_id,
            'text': text,
            'reply_markup': reply_markup
        }

        if not text:
            del data['text']

        return data, params

    def build_params(
            self,
            message: types.Message,
            user_lang: BaseLanguage,
            status: bool,
            token: str,
    ):
        web_app = WebAppInfo(
            url=f'{os.environ.get("WEB_URL")}/{user_lang.REQUEST_CODE}/home?'
                f'user_id={message.chat.id}&token={token}&started={status}'
        )

        params = [
            {'callback_data': f'bot_status:{status}', 'text': user_lang.STOP_BOT if status else user_lang.START_BOT},
            {'text': user_lang.FILTERS, 'web_app': web_app},
            {'callback_data': 'main_menu', 'text': user_lang.BACK},
        ]
        return params


class SupportBuilder(BaseNavigation):
    def __init__(self, button_column=1):
        super().__init__(User)

        self.button_column = button_column

    def build(
            self,
            message: types.Message,
            message_id: int,
            user_lang: BaseLanguage,
            text: str
    ):
        params = [
            {
                'callback_data': 'manager',
                'text': user_lang.MANAGER,
                'url': Support.MANAGER
            },
            {
                'callback_data': 'technical',
                'text': user_lang.TECHNICAL,
                'url': Support.TECHNICAL
            },
            {
                'callback_data': 'main_menu',
                'text': user_lang.BACK
            },
        ]
        reply_markup = Constructor.reply_markup(params=params, columns=self.button_column)

        data = {
            'chat_id': message.chat.id,
            'message_id': message.message_id,
            'text': user_lang.SUPPORT_SECTION,
            'reply_markup': reply_markup,
        }

        return data, params
