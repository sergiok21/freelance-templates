import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, Message, CallbackQuery

from bot_service.admin.start import start_admin
from bot_service.middlewares.router.class_register import register_outer_middleware_class, \
    register_callback_outer_middleware_class
from shared.utils.message import delete_or_update_message
from shared.common.states.admin import AdminStates
from shared.common.states.user import LoadUser
from shared.database.models import User, Admin
from bot_service.user.start import start_user

logger = logging.getLogger(__name__)


@register_outer_middleware_class
class PrivateChatMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        event: Message
        if event.chat.type != 'private':
            logger.info(f'Chat id {event.chat.id} is not private')
            return
        return await handler(event, data)


@register_outer_middleware_class
class MessageDeleterMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        instance = event.message if isinstance(event, CallbackQuery) else event
        self.t_id, self.message_id, self.text, self.state = \
            instance.chat.id, instance.message_id, instance.text, data['state']
        logger.info(f'Deleting message {self.t_id}: {self.text}')
        try:
            await event.bot.delete_message(chat_id=self.t_id, message_id=self.message_id)
        except TelegramBadRequest:
            pass
        return await handler(event, data)


@register_callback_outer_middleware_class
class CallbackDeleterMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        instance = event.message
        self.t_id, self.message_id, self.text, self.state = \
            instance.chat.id, instance.message_id, instance.text, data['state']
        if await self._is_message_id_not_valid():
            logger.info(f'Deleting callback message {self.t_id}: {self.text}')
            user_lang = await User(t_id=self.t_id).get_language()
            await delete_or_update_message(chat_id=self.t_id, message_id=self.message_id, user_lang=user_lang)
            return
        return await handler(event, data)

    async def _is_message_id_not_valid(self) -> bool:
        if await Admin(t_id=self.t_id).get_message_id():
            return await Admin(t_id=self.t_id).get_message_id() != self.message_id
        if await User(t_id=self.t_id).get_message_id():
            return await User(t_id=self.t_id).get_message_id() != self.message_id
        return False


@register_outer_middleware_class
class StartUserMiddleware(BaseMiddleware):
    def __init__(self):
        self.t_id: int
        self.text: str
        self.state: FSMContext

    async def __call__(
            self,
            handler:
            Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        self.t_id, self.message_id, self.text, self.state = event.chat.id, event.message_id, event.text, data['state']
        if not await User(t_id=self.t_id).is_user_exists() and not await Admin(t_id=self.t_id).is_admin_exists():
            return await start_user(event, self.state)
        elif self.text in ['/start', '/home']:
            return await self._start_command_process(
                message=event, state=self.state
            )
        return await handler(event, data)

    async def _start_command_process(self, message: Message, state: FSMContext):
        if await Admin(t_id=self.t_id).is_admin_exists():
            if await AdminStates.is_admin_inited(t_id=self.t_id):
                return await AdminStates.redirect_to_home_page(message=message)
            return await start_admin(callback=message, state=state)
        elif await User(t_id=self.t_id).get_token_data() and self.text in ['/home', '/start']:
            return await LoadUser.current_state(message=message, state=state)
        elif self.text == '/start':
            return await start_user(message=message, state=state)
