from functools import wraps

from aiogram.types import CallbackQuery, Message

from shared.common.configs.bot import models


def is_admin(func):
    @wraps(func)
    async def wrapper(callback: Message | CallbackQuery, *args, **kwargs):
        if isinstance(callback, CallbackQuery):
            instance = callback.message
        else:
            instance = callback
        if await models.admins[instance.chat.id].is_admin_exists():
            return await func(callback, *args, **kwargs)
        return
    return wrapper
