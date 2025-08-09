import logging

from aiogram.exceptions import TelegramForbiddenError

from shared.common.states.user import DropUser
from shared.common.configs.bot import bot
from shared.database.models import User

logger = logging.getLogger(__name__)


async def payment_reminder_task(t_id):
    logger.info(f'Started payment reminder task for user {t_id}. '
                f'Payment reminder status: {await User(t_id=t_id).get_payment()}')
    if await User(t_id=t_id).get_payment():
        user_lang, expiration_date = await User(t_id=t_id).get_language(), await User(t_id=t_id).get_token_date()
        try:
            send_message_response = await bot.send_message(
                chat_id=t_id, text=user_lang.PAYMENT_NOTIFICATION.format(expiration_date)
            )
            message_id = send_message_response.message_id
            await bot.pin_chat_message(chat_id=t_id, message_id=message_id)
            logger.info(f'Reminder payment message was sent for user {t_id}')

            await User(t_id=t_id).delete_notice_task()
            logger.info(f'User reminder task {t_id} was deleted')

        except TelegramForbiddenError as ex:
            logger.error(f'Got Telegram Forbidden Error for user {t_id}: {ex.message}')


async def drop_user_task(t_id: int, data: dict, params: list):
    user_model = User(t_id=t_id)
    if data.get('message_id'):
        del data['message_id']
    user_lang, message_id = await user_model.get_language(), await user_model.get_message_id()

    await DropUser.drop_user(
        user_model=user_model, message_id=message_id, data=data, params=params, user_lang=user_lang
    )
    logger.info(f'User {user_model.t_id} was dropped')

    await User(t_id=t_id).delete_drop_task()
    logger.info(f'User drop task {t_id} was deleted')
