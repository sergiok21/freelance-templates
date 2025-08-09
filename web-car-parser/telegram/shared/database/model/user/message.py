from typing import List, Dict

from shared.database.model.base import BaseModel
from shared.database.core import Redis


class MessageData(BaseModel):
    async def get_message_data(self) -> dict:
        return await Redis.get(key='users', path=f'.{self.t_id}.message.data')

    async def set_message_data(self, data) -> None:
        await Redis.set(key='users', path=f'.{self.t_id}.message.data', data=data)


class MessageParams(BaseModel):
    async def get_message_params(self) -> list:
        return await Redis.get(key='users', path=f'.{self.t_id}.message.params')

    async def set_message_params(self, data: List[dict]) -> None:
        await Redis.set(key='users', path=f'.{self.t_id}.message.params', data=data)


class MessageID(BaseModel):
    async def get_message_id(self) -> int:
        return await Redis.get(key='users', path=f'.{self.t_id}.message.data.message_id')

    async def set_message_id(self, data: int) -> None:
        await Redis.set(key='users', path=f'.{self.t_id}.message.data.message_id', data=data)


class UserMessage(MessageData, MessageParams, MessageID):
    async def get_message(self) -> dict:
        return await Redis.get(key='users', path=f'.{self.t_id}.message')

    async def set_message(self, data: Dict[str, dict | list]) -> None:
        await Redis.set(key='users', path=f'.{self.t_id}.message', data=data)
