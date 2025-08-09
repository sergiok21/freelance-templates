from uuid import uuid4

from shared.database.model.base import BaseModel
from shared.database.core import Redis


class Token(BaseModel):
    async def get_token_data(self):
        return await Redis.get(key='admins', path=f'.tokens')

    async def get_tokens(self):
        tokens = await Redis.get(key='admins', path=f'.tokens')
        return list(tokens.keys())

    async def set_token(self, token: uuid4, period: str):
        await Redis.set(key='admins', path=f'.tokens.{token}', data=period)

    async def delete_token(self, token: str):
        try:
            await Redis.delete(key='admins', path=f'.tokens.{token}')
        except ValueError:
            pass

    async def get_token_task(self, token: str = None):
        if token:
            return await Redis.get(key='admins', path=f'.tasks.{token}')
        return await Redis.get(key='admins', path=f'.tasks')

    async def set_token_task(self, token: uuid4, job_id: str):
        await Redis.set(key='admins', path=f'.tasks.{token}', data=job_id)

    async def delete_token_task(self, token: str):
        try:
            await Redis.delete(key='admins', path=f'.tasks.{token}')
        except ValueError:
            pass


class AdminTelegram(Token):
    async def is_admin_exists(self) -> bool:
        return bool(await Redis.get(key='admins', path=f'.{self.t_id}'))

    async def get_admins_telegram_id(self) -> list:
        admins = await Redis.get(key='admins')
        return list(admins.keys())

    async def get_users_telegram_id(self, from_=0, to_=1) -> list:
        users = await Redis.get(key='users')
        if to_ > 1:
            return list(users.keys())[from_:to_]
        return list(users.keys())
