import logging
import re

from shared.common.configs.bot import dp
from bot_service.middlewares.router.class_register import middlewares_container, \
    outer_middlewares_container, callback_middlewares_container, \
    callback_outer_middlewares_container

logger = logging.getLogger(__name__)


class BaseMiddlewareRegister:
    async def registration(self):
        method_names = [
            method for method in dir(self)
            if callable(getattr(self, method)) and re.search(r'^(?!__.*|registration)', method)
        ]
        for method_name in method_names:
            method = getattr(self, method_name)
            await method()


class GeneralMiddlewareRegister(BaseMiddlewareRegister):
    def __init__(self):
        super().__init__()
    
    async def middlewares_register(self):
        for cls in middlewares_container:
            dp.message.middleware.register(cls())

    async def outer_middlewares_register(self):
        for cls in outer_middlewares_container:
            dp.message.outer_middleware.register(cls())

    async def callback_middlewares_register(self):
        for cls in callback_middlewares_container:
            dp.callback_query.middleware.register(cls())

    async def callback_outer_middlewares_register(self):
        for cls in callback_outer_middlewares_container:
            dp.callback_query.outer_middleware.register(cls())
