import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from bot_service.middlewares.router.class_register import register_outer_middleware_class, \
    register_callback_outer_middleware_class
from shared.common.configs.bot import models
from shared.database.models import User, Admin

logger = logging.getLogger(__name__)


class BaseRegister:
    async def register_user_or_admin(self, t_id: int):
        if t_id not in models.users and t_id not in models.admins:
            user, admin = User(t_id=t_id), Admin(t_id=t_id)
            if await admin.is_admin_exists() and not models.admins.get(t_id):
                models.admins[t_id] = admin
                logger.info(f'Admin model for {t_id} was created')
            else:
                models.users[t_id] = user
                logger.info(f'User model for {t_id} was created')


@register_outer_middleware_class
class UserModelMiddleware(BaseMiddleware, BaseRegister):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        event: Message
        await self.register_user_or_admin(t_id=event.chat.id)
        return await handler(event, data)


@register_callback_outer_middleware_class
class CallbackUserModelMiddleware(BaseMiddleware, BaseRegister):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        await self.register_user_or_admin(t_id=event.message.chat.id)
        return await handler(event, data)
