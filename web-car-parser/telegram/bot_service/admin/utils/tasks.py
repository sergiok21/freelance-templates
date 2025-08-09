import logging
from uuid import uuid4

from shared.common.configs.redis import tokens_queue
from shared.database.models import Task, Admin
from shared.utils.date import Date

logger = logging.getLogger(__name__)


class Token:
    @staticmethod
    async def delete_token(t_id: int, token: uuid4):
        specific_time = Date.create_date(days=1)
        description = f'Delete token | Token: {str(token)}.'
        meta = {
            'function': 'tasks.admin.delete_token_task',
            'args': (t_id, str(token),),
            'date': Date.transform_to_standard_date(date=specific_time),
        }

        job = Task.create(
            enqueue=tokens_queue.enqueue_at, datetime=specific_time,
            f='tasks.admin.delete_token_task', args=(t_id, token,),
            description=description, meta=meta
        )
        await Admin(t_id=t_id).set_token_task(token=str(token), job_id=job.id)

        logger.info(f'Created task to delete token by {t_id}')
