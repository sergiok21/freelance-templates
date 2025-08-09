from shared.database.model.base import BaseModel
from shared.database.core import Redis


class UserStatus(BaseModel):
    async def get_state(self) -> str:
        return await Redis.get(key='users', path=f'.{self.t_id}.state')

    async def set_state(self, data):
        await Redis.set(key='users', path=f'.{self.t_id}.state', data=data)

    async def get_drop_task(self):
        return await Redis.get(key='users', path=f'.{self.t_id}.drop_task')

    async def set_drop_task(self, data: str):
        await Redis.set(key='users', path=f'.{self.t_id}.drop_task', data=data)

    async def delete_drop_task(self):
        await Redis.delete(key='users', path=f'.{self.t_id}.drop_task')
