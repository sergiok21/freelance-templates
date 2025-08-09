import logging

from aiogram import F, types

from bot_service.user.utils.tasks import Notices
from shared.common.configs.bot import profile_router, bot, models
from shared.constructor.user import NoticeBuilder
from shared.database.models import Task
from shared.utils.date import Date

logger = logging.getLogger(__name__)


@profile_router.callback_query(F.data == 'notices')
async def notices_callback(callback: types.CallbackQuery):
    user_lang = await models.users[callback.message.chat.id].get_language()
    payment = await models.users[callback.message.chat.id].get_payment()
    text = f'{user_lang.REMINDER_TEXT}\n\n' \
           f'{user_lang.NOTICES_SECTION}'

    data, params = NoticeBuilder(button_column=2).build(
        message=callback.message, message_id=callback.message.message_id,
        user_lang=user_lang, text=text, payment=payment
    )
    await bot.edit_message_text(**data)


@profile_router.callback_query(F.data.startswith('notices:payment'))
async def payment_status_callback(callback: types.CallbackQuery):
    user_lang = await models.users[callback.message.chat.id].get_language()

    split_data = callback.data.split(':')
    reminder_type, status = split_data[1], not split_data[2] == 'True'

    data, params = NoticeBuilder(button_column=2).build(
        message=callback.message, message_id=callback.message.message_id, user_lang=user_lang, payment=status
    )

    await bot.edit_message_reply_markup(**data)
    await models.users[callback.message.chat.id].set_payment(data=status)

    job_id = await models.users[callback.message.chat.id].get_notice_task()
    Task.delete(job_id=job_id)
    if status:
        current_date = await models.users[callback.message.chat.id].get_token_date()
        date = Date.update_date(date=current_date, days=-3)
        await Notices.set_payment_reminder(message=callback.message, date=date)

    logger.info(f'User {callback.message.chat.id} changed payment notice to {status}')
