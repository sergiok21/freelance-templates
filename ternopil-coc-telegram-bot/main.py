import asyncio
import logging

from commands import set_user_commands, set_admin_commands
from config.bot import bot, router
from config.bot import dp

from handlers.account import add_account, remove_account
from handlers.poll import create_poll
from handlers.views import table_empty_answers_command

"""
При додаванні нового хендлера (handlers), робити його імпорт тут!
"""

logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Основна точка входу для запуску Telegram-бота.

    Процес включає:
    - Реєстрацію роутерів у диспетчері повідомлень.
    - Встановлення команд для користувачів і адміністраторів.
    - Запуск довготривалого опитування оновлень від Telegram через бота.

    :return: None
    """
    dp.include_router(router)

    await set_admin_commands()
    await set_user_commands()

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Exiting...')
