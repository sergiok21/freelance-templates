from shared.common.configs.logger import *

import json
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import redis.asyncio as aioredis
from aiogram.methods.get_updates import GetUpdates

from shared.database.models import Models
from shared.common.middlewares.session import SessionLoggingMiddleware
from shared.common.storage.key_builder import CustomKeyBuilder
from shared.common.storage.redis import RedisJSONStorage


# Bot
token = '...'

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(
    bot=bot, storage=RedisJSONStorage(
        redis=aioredis.from_url('redis://...'), key_builder=CustomKeyBuilder(),
        json_dumps=json.dumps, json_loads=json.loads
    )
)

bot_headers = {
    'Authorization': os.environ.get('TELEGRAM_TOKEN_SERVICE'),
}


# User routers
start_router = Router()
home_router = Router()
subscription_router = Router()
profile_router = Router()
bot_router = Router()

# Admin routers
admin_router = Router()

# All routers
routers = [
    start_router, home_router, subscription_router, profile_router, bot_router, admin_router
]

# Start routers
start_routers = [
    start_router
]

# Profile routers
profile_routers = [
    home_router, subscription_router, profile_router, bot_router
]


# Middlewares
bot.session.middleware(SessionLoggingMiddleware(ignore_methods=[GetUpdates]))


# Model
models = Models()


# Webhook
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET')

WEBHOOK_HOST = f"{os.environ.get('MAIN_URL')}/bot"
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 8080
