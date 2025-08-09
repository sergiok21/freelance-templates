from typing import Literal

from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import KeyBuilder

from shared.database.models import Admin


class CustomKeyBuilder(KeyBuilder):
    async def build(self, key: StorageKey, part: Literal["data", "state", "lock"]) -> list:
        result_key = []
        if await Admin(t_id=key.chat_id).is_admin_exists():
            result_key.append('admins')
        else:
            result_key.append('users')
        result_key.append(f'.{key.chat_id}.{part}')
        return result_key
