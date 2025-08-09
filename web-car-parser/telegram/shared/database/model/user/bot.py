from shared.database.model.base import BaseModel
from shared.database.core import Redis


class UserBotStatus(BaseModel):
    async def get_bot_status(self) -> bool:
        return await Redis.get(key='users', path=f'.{self.t_id}.bot.status')

    async def set_bot_status(self, data: bool) -> None:
        await Redis.set(key='users', path=f'.{self.t_id}.bot.status', data=data)


class UserBot(UserBotStatus):
    async def create_bot(self) -> None:
        await Redis.set(key='users', path=f'.{self.t_id}.bot', data={'status': False})
