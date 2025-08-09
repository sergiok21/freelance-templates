import os

import redis as rds
from rq import Queue


redis = rds.Redis().from_url(url=os.environ.get('REDIS_URL'))

notices_queue = Queue(name='notices', connection=redis)
users_queue = Queue(name='users', connection=redis)
tokens_queue = Queue(name='tokens', connection=redis)
service_queue = Queue(name='service', connection=redis)
