import logging
from typing import Any, Optional, List, Type

from aiogram import loggers

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.exceptions import TelegramNetworkError
from aiogram.methods.base import TelegramMethod, TelegramType, Response
from aiogram.client.session.middlewares.base import NextRequestMiddlewareType


logger = logging.getLogger(__name__)


class SessionLoggingMiddleware(BaseMiddleware):
    def __init__(self, ignore_methods: Optional[List[Type[TelegramMethod[Any]]]] = None):
        """
        Middleware for logging outgoing requests

        :param ignore_methods: methods to ignore in logging middleware
        """
        self.ignore_methods = ignore_methods if ignore_methods else []

    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[TelegramType],
        bot: "Bot",
        method: TelegramMethod[TelegramType],
    ) -> Response[TelegramType]:
        if type(method) not in self.ignore_methods:
            loggers.middlewares.info(
                "Make request with method=%r by bot id=%d",
                type(method).__name__,
                bot.id,
            )
        try:
            return await make_request(bot, method)
        except TelegramNetworkError:
            return await make_request(bot, method)
