import logging

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, BotCommandScopeChat

from bot_service.admin.commands import set_admin_commands
from shared.common.configs.bot import models, bot
from shared.constructor.admin import StartBuilder
from shared.utils.localization import ADMIN
from shared.common.states.base import BaseState
from shared.utils.bot import resend_bot_message

logger = logging.getLogger(__name__)


class AdminStates(StatesGroup, BaseState):
    DELETE_MESSAGE = State()

    @staticmethod
    async def redirect_to_home_page(message: Message):
        await set_admin_commands(chat_id=message.chat.id)

        message_id = await models.admins[message.chat.id].get_message_id()
        data, params = StartBuilder().build(
            message=message, message_id=message_id, text=ADMIN.MAIN_MENU
        )
        await resend_bot_message(
            model=models.admins[message.chat.id], data=data, params=params
        )

        logger.info(f'Admin with ID {message.chat.id} was redirected to home page')

    @staticmethod
    async def is_admin_inited(t_id) -> bool:
        return bool(await models.admins[t_id].get_message_id())
