import logging
import os

from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters.state import State, StatesGroup
from aiogram.types import BotCommandScopeChat

from shared.common.configs.redis import service_queue
from shared.database.models import Task
from shared.utils.date import Date
from shared.utils.localization import BaseLanguage
from shared.utils.message import delete_or_update_message
from shared.utils.request import Sender, Request
from shared.common.states.base import BaseState
from aiogram import types
from aiogram.fsm.context import FSMContext
from shared.common.configs.bot import bot, models, bot_headers
from shared.constructor.base import Constructor
from shared.utils.bot import resend_bot_message

logger = logging.getLogger(__name__)


class UserStates(StatesGroup, BaseState):
    START = State()
    ACTIVATION = State()
    DELETE_MESSAGE = State()
    MAIN_MENU = State()
    UPDATE_SUBSCRIPTION = State()


class LoadUser:
    @staticmethod
    async def current_state(message: types.Message, state: FSMContext):
        await state.set_state(state=UserStates.DELETE_MESSAGE)

        message_data = await models.users[message.chat.id].get_message()
        data, params = message_data['data'], message_data['params']
        data['reply_markup'] = Constructor.reply_markup(params=params, columns=1)

        await resend_bot_message(
            model=models.users[message.chat.id], data=data, params=params
        )

        logger.info(f'User {message.chat.id} was successfully loaded')


class UpdateUser:
    @staticmethod
    def update_web_data(headers: dict, t_id: str, token: str):
        logger.error(f'Web service is not responding while proceeding update web data')

        specific_time = Date.create_date(seconds=5)
        description = f'Update web data | User ID: {t_id}'
        meta = {
            'function': 'tasks.service.update_web_data_task',
            'args': (headers, str(t_id), token),
            'date': Date.transform_to_standard_date(date=specific_time),
        }

        Task.create(
            enqueue=service_queue.enqueue_at, datetime=specific_time,
            f='tasks.service.update_web_data_task',
            args=(headers, str(t_id), token),
            description=description, meta=meta
        )

        logger.info(f'Created task to delete user data in web service {t_id}')


class DropUser:
    @staticmethod
    async def drop_user(user_model, message_id: int, data: dict, params: list, user_lang: BaseLanguage):
        await delete_or_update_message(chat_id=user_model.t_id, message_id=message_id, user_lang=user_lang)
        await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=user_model.t_id))

        try:
            reply_markup = Constructor.reply_markup(params=params, columns=1)
            response = await bot.send_message(reply_markup=reply_markup, **data)
            data['message_id'] = response.message_id
        except TelegramForbiddenError as ex:
            logger.info(f'Got error while proceeding drop user task: {ex.message}')
            data['message_id'] = message_id

        await user_model.set_state(data='UserStates:ACTIVATION')
        await DropUser._save(user_model=user_model, data=data, params=params)

    @staticmethod
    def _delete_web_data(user_model):
        if not Sender.send_data_to_service(
                method=Request().delete, headers=bot_headers, t_id=user_model.t_id
        ):
            logger.error(f'Web service is not responding while proceeding delete user token')

            specific_time = Date.create_date(hours=1)
            description = f'Delete web data | User ID: {user_model.t_id}'
            meta = {
                'function': 'tasks.service.delete_web_data_task',
                'args': (bot_headers, user_model.t_id),
                'date': Date.transform_to_standard_date(date=specific_time),
            }

            Task.create(
                enqueue=service_queue.enqueue_at, datetime=specific_time,
                f='tasks.service.delete_web_data_task',
                args=(bot_headers, user_model.t_id),
                description=description, meta=meta
            )

            logger.info(f'Created task to delete user data in web service {user_model.t_id}')

    @staticmethod
    def _delete_parser_data(user_model):
        if not Sender.send_data_to_service(
                method=Request().post, url=f'{os.environ.get("PARSER_URL")}/api/parser/status/',
                headers=bot_headers, user_status={'status': False, 'user_id': user_model.t_id}
        ):
            logger.error(f'Parser service is not responding while proceeding delete parser threads')

            specific_time = Date.create_date(hours=1)
            description = f'Delete parser data | User ID: {user_model.t_id}'
            meta = {
                'function': 'tasks.service.delete_parser_data_task',
                'args': (
                    f'{os.environ.get("PARSER_URL")}/api/parser/status/',
                    bot_headers,
                    {'status': False, 'user_id': user_model.t_id}),
                'date': Date.transform_to_standard_date(date=specific_time),
            }

            Task.create(
                enqueue=service_queue.enqueue_at, datetime=specific_time,
                f='tasks.service.delete_parser_data_task',
                args=(
                    f'{os.environ.get("PARSER_URL")}/api/parser/status/',
                    bot_headers,
                    {'status': False, 'user_id': user_model.t_id}
                ),
                description=description, meta=meta
            )

            logger.info(f'Created task to delete user threads in parser service {user_model.t_id}')

    @staticmethod
    async def _save(user_model, data, params):
        await user_model.set_message(data={'data': data, 'params': params})
        await user_model.set_bot_status(data=False)
        await user_model.delete_token_data()

        DropUser._delete_web_data(user_model=user_model)
        DropUser._delete_parser_data(user_model=user_model)
