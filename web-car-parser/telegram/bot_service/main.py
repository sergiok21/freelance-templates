from aiohttp import web

from shared.common.configs.bot import bot, WEBHOOK_PATH, WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT
from webhook import Updater, prepare_dispatcher
from shared.common.configs.bot import WEBHOOK_SECRET


async def on_startup(app: web.Application):
    await prepare_dispatcher()
    await bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET)


async def on_shutdown(app: web.Application):
    await bot.delete_webhook()


def config_app():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, Updater().process_webhook_updates)
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_shutdown)
    return app


if __name__ == '__main__':
    try:
        app = config_app()
        web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
    except KeyboardInterrupt:
        pass
