from aiogram import types
from aiohttp import web

from bot_service.middlewares.router.middleware_register import GeneralMiddlewareRegister
from shared.common.configs.bot import bot, dp, routers, WEBHOOK_SECRET


class Updater:
    async def process_webhook_updates(self, request):
        token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
        if token and token == WEBHOOK_SECRET:
            data = await request.json()
            update = types.Update(**data)
            await dp.feed_webhook_update(bot, update)
            return web.Response()


async def prepare_dispatcher():
    await GeneralMiddlewareRegister().registration()
    for router in routers:
        dp.include_router(router)
