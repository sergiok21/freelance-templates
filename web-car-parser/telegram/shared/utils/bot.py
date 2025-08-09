import logging

from shared.utils.message import delete_or_update_message
from shared.common.configs.bot import bot
from shared.database.models import Admin

logger = logging.getLogger(__name__)


async def resend_bot_message(model, data: dict, params: list) -> int:
    if data.get('message_id'):
        del data['message_id']
    response = await bot.send_message(**data)
    try:
        if await model.get_bot_status():
            await bot.pin_chat_message(
                chat_id=response.chat.id, message_id=response.message_id, disable_notification=True
            )
    except AttributeError:
        pass

    old_message_id = await model.get_message_id()

    del data['reply_markup']
    data['message_id'] = response.message_id
    if isinstance(model, Admin):
        await delete_or_update_message(chat_id=data.get('chat_id'), message_id=old_message_id)
        logger.info(f'Old user message {data.get("chat_id")} was deleted or updated')
        await model.set_message(data=data)
    else:
        user_lang = await model.get_language()
        await delete_or_update_message(chat_id=data.get('chat_id'), message_id=old_message_id, user_lang=user_lang)
        logger.info(f'Old user message {data.get("chat_id")} was deleted or updated')
        await model.set_message(data={'data': data, 'params': params})

    logger.info(f'User or admin data {data.get("chat_id")} was saved')

    return response.message_id
