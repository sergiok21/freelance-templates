from typing import Type

from shared.database.model.base import BaseModel
from shared.database.core import Redis
from shared.utils.localization import LanguageProcessor, BaseLanguage


class UserLanguage(BaseModel):
    async def get_language(self) -> BaseLanguage:
        lang = await Redis.get(key='users', path=f'.{self.t_id}.user_data.lang')
        return LanguageProcessor.define_language(lang=lang)

    async def set_language(self, data: str) -> None:
        await Redis.set(key='users', path=f'.{self.t_id}.user_data.lang', data=data)
