import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import TelegramObject, CallbackQuery

from bot_service.middlewares.router.class_register import register_callback_outer_middleware_class

logger = logging.getLogger(__name__)


@register_callback_outer_middleware_class
class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        try:
            return await handler(event, data)
        except TelegramBadRequest as ex:
            logger.error(f'Request could not be processed: {ex.message}')
        except Exception as ex:
            logger.warning(f'Got another exception: {ex}')
