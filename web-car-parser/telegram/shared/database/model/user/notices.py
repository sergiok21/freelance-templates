from shared.database.model.base import BaseModel
from shared.database.core import Redis


class Mode(BaseModel):
    async def get_mode(self) -> dict:
        return await Redis.get(key='users', path=f'.{self.t_id}.notices.mode')

    async def set_mode(self, data: bool) -> None:
        await Redis.set(key='users', path=f'.{self.t_id}.notices.mode', data=data)


class Payment(BaseModel):
    async def get_payment(self) -> dict:
        return await Redis.get(key='users', path=f'.{self.t_id}.notices.payment')

    async def set_payment(self, data: bool) -> None:
        await Redis.set(key='users', path=f'.{self.t_id}.notices.payment', data=data)


class UserNotices(Payment, Mode):
    async def create_notices(self) -> None:
        await Redis.set(
            key='users', path=f'.{self.t_id}.notices', data={'payment': True, 'mode': False}
        )

    async def get_notices(self) -> dict:
        return await Redis.get(key='users', path=f'.{self.t_id}.notices')

    async def get_notice_task(self):
        return await Redis.get(key='users', path=f'.{self.t_id}.notices.task')

    async def set_notice_task(self, data: str):
        await Redis.set(key='users', path=f'.{self.t_id}.notices.task', data=data)

    async def delete_notice_task(self):
        await Redis.delete(key='users', path=f'.{self.t_id}.notices.task')
