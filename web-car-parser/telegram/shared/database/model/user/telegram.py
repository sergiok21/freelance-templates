from typing import Dict
from uuid import uuid4, UUID

from aiogram import Bot

from shared.database.model.base import BaseModel
from shared.database.core import Redis


class ID(BaseModel):
    async def get_t_id(self) -> int:
        return await Redis.get(key='users', path=f'.{self.t_id}.user_data.t_id')

    async def set_t_id(self, data: int) -> None:
        await Redis.set(key='users', path=f'.{self.t_id}.user_data.t_id', data=data)


class FirstName(BaseModel):
    async def get_first_name(self) -> str:
        return await Redis.get(key='users', path=f'.{self.t_id}.user_data.first_name')

    async def set_first_name(self, data: str) -> None:
        await Redis.set(key='users', path=f'.{self.t_id}.user_data.first_name', data=data)


class LastName(BaseModel):
    async def get_last_name(self) -> str:
        return await Redis.get(key='users', path=f'.{self.t_id}.user_data.last_name')

    async def set_last_name(self, data: str) -> None:
        await Redis.set(key='users', path=f'.{self.t_id}.user_data.last_name', data=data)


class Tag(BaseModel):
    async def get_tag(self) -> str:
        return await Redis.get(key='users', path=f'.{self.t_id}.user_data.tag')

    async def set_tag(self, data: str) -> None:
        await Redis.set(key='users', path=f'.{self.t_id}.user_data.tag', data=data)


class Token(BaseModel):
    async def is_token_exists(self, token: str | UUID) -> bool:
        return True \
            if await Redis.get(key='users', path=f'.{self.t_id}.user_data.token.{token}') else False

    async def get_token_data(self) -> dict:
        return await Redis.get(key='users', path=f'.{self.t_id}.user_data.token')

    async def set_token_data(self, data: Dict[str, str]) -> None:
        await Redis.set(key='users', path=f'.{self.t_id}.user_data.token', data=data)

    async def delete_token_data(self) -> None:
        await Redis.delete(key='users', path=f'.{self.t_id}.user_data.token')

    async def get_token(self) -> str:
        token = await Redis.get(key='users', path=f'.{self.t_id}.user_data.token')
        return None if not token else list(token.keys())[0]

    async def get_token_date(self) -> str:
        date = await Redis.get(key='users', path=f'.{self.t_id}.user_data.token')
        return None if not date else list(date.values())[0]


class UserTelegram(ID, FirstName, LastName, Tag, Token):
    async def is_user_exists(self) -> bool:
        user_data = await Redis.get(key='users', path=f'.{self.t_id}')
        return bool(user_data)

    async def get_telegram_data(self, bot: Bot) -> dict:
        general_info = await bot.get_chat(self.t_id)
        return {
            't_id': str(self.t_id),
            'tag': general_info.username,
            'first_name': general_info.first_name,
            'last_name': general_info.last_name,
            'token': {}
        }
