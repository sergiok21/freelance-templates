import logging
import os

import requests
from aiogram import types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from shared.utils.request import Sender, Request
from shared.constructor.user import BotBuilder
from shared.common.configs.bot import bot_router, bot, bot_headers, models
from shared.utils.localization import BaseLanguage

logger = logging.getLogger(__name__)


@bot_router.callback_query(F.data.startswith('bot_configuration'))
async def bot_configuration_callback(callback: types.CallbackQuery):
    user_lang = await models.users[callback.message.chat.id].get_language()
    status = await models.users[callback.message.chat.id].get_bot_status()
    token = await models.users[callback.message.chat.id].get_token()
    text = f'{user_lang.BOT_SETTINGS_SECTION}'

    data, params = BotBuilder().build(
        message=callback.message, message_id=callback.message.message_id, user_lang=user_lang,
        text=text, status=status, token=token
    )

    await bot.edit_message_text(**data)


@bot_router.callback_query(F.data.startswith('bot_status'))
async def status_bot_callback(callback: types.CallbackQuery, state: FSMContext):
    user_lang = await models.users[callback.message.chat.id].get_language()
    token = await models.users[callback.message.chat.id].get_token()
    status = not await models.users[callback.message.chat.id].get_bot_status()

    data, params = BotBuilder().build(
        message=callback.message, message_id=callback.message.message_id, user_lang=user_lang,
        status=status, token=token
    )

    status_code = Sender.send_data_to_service(
        method=Request().post, url=f'{os.environ.get("PARSER_URL")}/api/parser/status/',
        headers=bot_headers, user_status={'status': status, 'user_id': callback.message.chat.id}
    )

    if status_code == 204:
        logger.info(f'User {callback.message.chat.id} was {"started" if status else "stopped"} the bot')
    else:
        await callback.answer(text=f'{user_lang.SERVICE_DOES_NOT_WORK} ({status_code})')
        logger.error(f'{"Start" if status else "Stop"} user bot {callback.message.chat.id} was wrong. '
                     f'Parser service status: {status_code}')
        await send_status_to_web_service(message=callback.message, status=status)

    try:
        await process_status(callback=callback, data=data, user_lang=user_lang, status=status)
    except TelegramBadRequest:
        pass


async def process_status(callback: types.CallbackQuery, data: dict, user_lang: BaseLanguage, status: bool):
    await bot.edit_message_reply_markup(**data)
    await callback.answer(
        text=user_lang.BOT_RUNNING if status else user_lang.BOT_STOPPING
    )
    if status:
        await bot.pin_chat_message(
            chat_id=callback.message.chat.id, message_id=callback.message.message_id, disable_notification=True
        )
    else:
        await bot.unpin_chat_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await models.users[callback.message.chat.id].set_bot_status(data=status)
    logger.info(f'Bot status was updated for user {callback.message.chat.id}')


async def send_status_to_web_service(message: types.Message, status: bool):
    token = await models.users[message.chat.id].get_token()
    headers = {'Authorization': token, 'User-Id': str(message.chat.id)}

    response = requests.get(url=f'{os.environ.get("WEB_URL")}/api/filters/', headers=headers)
    if response.status_code == 200:
        for item in response.json():
            Sender.send_data_to_service(
                method=Request().patch,
                url=f'{os.environ.get("PARSER_URL")}/api/filters/{item.get("id")}/',
                headers=headers,
                status=status
            )
        logger.info(f'Data was updated in web service for user {message.chat.id}')
