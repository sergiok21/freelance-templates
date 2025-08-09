import logging
from uuid import uuid4

from aiogram import types, F

from bot_service.admin.utils.tasks import Token
from shared.constructor.admin import CreateTokenBuilder, SetTokenDateBuilder
from bot_service.admin.utils.validators import is_admin
from shared.common.configs.bot import bot, admin_router, models
from shared.utils.localization import ADMIN
from shared.utils.date import Date

logger = logging.getLogger(__name__)


@admin_router.callback_query(F.data == 'create_token')
@is_admin
async def create_token_callback(callback: types.CallbackQuery):
    text = ADMIN.SET_MONTH

    data, params = CreateTokenBuilder(button_column=2).build(
        message=callback.message, message_id=callback.message.message_id, text=text
    )

    await bot.edit_message_text(**data)


@admin_router.callback_query(F.data.in_(['1', '3', '6', '12']))
@is_admin
async def set_token_date_callback(callback: types.CallbackQuery):
    token, show_time = uuid4(), Date.create_date(months=int(callback.data), transform=True)
    await models.admins[callback.message.chat.id].set_token(token=token, period=callback.data)
    text = ADMIN.TOKEN_CREATED.format(str(token), show_time)

    data, params = SetTokenDateBuilder().build(
        message=callback.message, message_id=callback.message.message_id, text=text
    )

    await bot.edit_message_text(**data)

    logger.info(f'Admin {callback.message.chat.id} was created token {token}')

    await Token.delete_token(t_id=callback.message.chat.id, token=token)
