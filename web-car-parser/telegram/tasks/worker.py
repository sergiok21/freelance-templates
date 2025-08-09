import logging

from rq import Worker

from shared.common.configs.redis import redis, notices_queue, tokens_queue, users_queue, service_queue
from .user import payment_reminder_task, drop_user_task
from .service import delete_web_data_task, delete_parser_data_task

logger = logging.getLogger(__name__)

worker = Worker([notices_queue, tokens_queue, users_queue, service_queue], connection=redis)
worker.work(with_scheduler=True)
