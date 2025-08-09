from typing import Optional

from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.redis import RedisStorage

from shared.database.core import Redis


class RedisJSONStorage(RedisStorage):
    async def set_state(self, key: StorageKey, state: Optional[str] = None) -> None:
        key, path = await self.key_builder.build(key, 'state')
        if state is None:
            await Redis.delete(key=key, path=path)
        else:
            await Redis.set(key=key, path=path, data=state.state)

    async def get_state(self, key: StorageKey) -> Optional[str]:
        key, path = await self.key_builder.build(key, 'state')
        try:
            state_data = await Redis.get(key=key, path=path)
            return state_data if not None else None
        except AttributeError:
            return None

    async def clear(self, key: StorageKey):
        pass
