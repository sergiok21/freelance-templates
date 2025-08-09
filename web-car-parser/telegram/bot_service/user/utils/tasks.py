import logging
from datetime import datetime

from aiogram import types
from rq.job import Job

from shared.common.configs.bot import models
from shared.common.configs.redis import notices_queue, users_queue
from shared.constructor.user import ActivateAccountBuilder
from shared.database.models import Task
from shared.utils.date import Date
from shared.utils.localization import BaseLanguage

logger = logging.getLogger(__name__)


class Notices:
    @staticmethod
    async def set_payment_reminder(message: types.Message, date: datetime):
        logger.info(f'Created time: {date}')
        description = f'Payment reminder | User ID: {message.chat.id}'
        meta = {
            'function': 'tasks.user.drop_user_task',
            'args': (message.chat.id,),
            'date': Date.transform_to_standard_date(date=date),
        }

        job = Task.create(
            enqueue=notices_queue.enqueue_at, datetime=date,
            f='tasks.user.payment_reminder_task', args=(message.chat.id,),
            description=description, meta=meta
        )

        await models.users[message.chat.id].set_notice_task(data=job.id)

        logger.info(f'Created reminder task for user {message.chat.id} ({job.id})')

    @staticmethod
    async def update_payment_reminder(message: types.Message, date: datetime):
        job_id = await models.users[message.chat.id].get_notice_task()
        if job_id:
            Task.delete(job_id=job_id)
            await Notices.set_payment_reminder(message=message, date=date)


class State:
    @staticmethod
    async def set_drop_user(message: types.Message, user_lang: BaseLanguage, date: datetime) -> Job:
        data, params = ActivateAccountBuilder().build(
            message=message, message_id=message.message_id,
            user_lang=user_lang, text=user_lang.RENEW_SUBSCRIPTION_PROCESS
        )
        del data['message_id']
        del data['reply_markup']

        description = f'Drop user | User ID: {message.chat.id}'
        meta = {
            'function': 'tasks.user.drop_user_task',
            'args': (message.chat.id, data, params),
            'date': Date.transform_to_standard_date(date=date),
        }
        job = Task.create(
            enqueue=users_queue.enqueue_at, datetime=date,
            f='tasks.user.drop_user_task', args=(message.chat.id, data, params),
            description=description, meta=meta
        )

        await models.users[message.chat.id].set_drop_task(data=job.id)
        logger.info(f'Drop user task {job.id} was created for user {message.chat.id}')

        return job

    @staticmethod
    async def update_drop_user(message: types.Message, user_lang: BaseLanguage, date: datetime | int):
        job_id = await models.users[message.chat.id].get_drop_task()
        if job_id:
            Task.delete(job_id=job_id)

            job = await State.set_drop_user(message=message, user_lang=user_lang, date=date)
            logger.info(f'Drop user task {job.id} was updated for user {message.chat.id}')

            return job
