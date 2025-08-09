from shared.database.model.base import BaseModel
from shared.database.core import Redis


class MessageID(BaseModel):
    async def get_message_id(self) -> int:
        return await Redis.get(key='admins', path=f'.{self.t_id}.message.message_id')

    async def set_message_id(self, data) -> int:
        return await Redis.set(key='admins', path=f'.{self.t_id}.message.message_id', data=data)


class AdminMessage(MessageID):
    async def get_message(self) -> dict:
        return await Redis.get(key='admins', path=f'.{self.t_id}.message')

    async def set_message(self, data: dict = None) -> dict:
        return await Redis.set(key='admins', path=f'.{self.t_id}.message', data=data if data else {})
