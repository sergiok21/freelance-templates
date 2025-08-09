import logging
from typing import Dict

from rq.exceptions import NoSuchJobError
from rq.job import Job

from shared.common.configs.redis import redis
from shared.database.model.admin.message import AdminMessage
from shared.database.model.admin.telegram import AdminTelegram
from shared.database.core import Redis
from shared.database.model.user.message import UserMessage
from shared.database.model.user.telegram import UserTelegram
from shared.database.model.user.notices import UserNotices
from shared.database.model.user.status import UserStatus
from shared.database.model.user.language import UserLanguage
from shared.database.model.user.bot import UserBot

logger = logging.getLogger(__name__)


class User(UserMessage, UserTelegram, UserNotices, UserStatus, UserLanguage, UserBot):
    async def create(self, data: dict = None):
        await Redis.set(
            key='users', path=f'.{self.t_id}', data=data if data else {}
        )

    async def get_all_users(self):
        return await Redis.get(key='users', path='.')

    async def get_all_data(self):
        return await Redis.get(key='users', path=f'.{self.t_id}')

    async def delete(self):
        await Redis.delete(key='users', path=f'.{self.t_id}')


class Admin(AdminMessage, AdminTelegram):
    async def get_all_admins(self):
        return await Redis.get(key='admins', path='.')

    async def get_all_data(self):
        return await Redis.get('admins', path=f'.{self.t_id}')


class Task:
    @staticmethod
    def create(enqueue, **kwargs) -> Job:
        return enqueue(result_ttl=172800, **kwargs)

    @staticmethod
    def get(job_id: str) -> Job:
        return Job.fetch(id=job_id, connection=redis)

    @staticmethod
    def update(job_id: str, *args):
        try:
            job = Job.fetch(id=job_id, connection=redis)
            if job.is_scheduled:
                job.args = args
                job.save()
                logger.info(f'Job {job_id} was updated in task model')
            logger.info(f'Job {job_id} was not updated cause job is not scheduled')
        except NoSuchJobError:
            logger.info(f'Job to update {job_id} was not found')

    @staticmethod
    def cancel(job_id: str):
        try:
            job = Job.fetch(id=job_id, connection=redis)
            if job.is_scheduled:
                job.cancel()
                logger.info(f'Job {job_id} was canceled in task model')
            logger.info(f'Job {job_id} was not canceled cause job is not scheduled')
        except NoSuchJobError:
            logger.info(f'Job to cancel {job_id} was not found')

    @staticmethod
    def delete(job_id: str):
        try:
            job = Job.fetch(id=job_id, connection=redis)
            job.delete()
            logger.info(f'Job {job_id} was deleted')
        except NoSuchJobError:
            logger.info(f'Job to delete {job_id} was not found')


class Models:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._users: Dict[int, User] = {}
            self._admins: Dict[int, Admin] = {}
            self._initialized = True

    @property
    def users(self):
        return self._users

    @users.setter
    def users(self, value):
        self._users = value

    @property
    def admins(self):
        return self._admins

    @admins.setter
    def admins(self, value):
        self._admins = value
