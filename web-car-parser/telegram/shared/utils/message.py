import logging

from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from shared.common.configs.bot import bot
from shared.utils.localization import BaseLanguage

logger = logging.getLogger(__name__)


async def delete_or_update_message(chat_id: int, message_id: int, user_lang=BaseLanguage):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except TelegramBadRequest:
        try:
            await bot.unpin_chat_message(chat_id=chat_id, message_id=message_id)
            await bot.edit_message_text(
                chat_id=chat_id, message_id=message_id, text=user_lang.OLD_MESSAGE
            )
        except TelegramBadRequest as ex:
            logger.info(f'Deleting or updating target message can not proceed: {ex.message}')
    except TelegramForbiddenError as ex:
        logger.info(f'Deleting or updating target message can not proceed: {ex.message}')
