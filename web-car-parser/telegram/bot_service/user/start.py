import logging

from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommandScopeChat

from shared.constructor.user import StartBuilder
from shared.common.states.user import UserStates
from shared.common.configs.bot import start_router, bot, models
from shared.utils.bot import resend_bot_message
from shared.utils.date import Date
from shared.utils.localization import ENG

logger = logging.getLogger(__name__)


class Saver:
    def __init__(self, model):
        self.model = model

    async def save_language(self):
        user_data = await self.model.get_telegram_data(bot=bot)
        user_data.update({'lang': 'eng', 'created': Date.get_current_date(transform=True)})
        await self.model.create(data={'user_data': user_data})

    async def save_started_data(self, data, params, response):
        del data['reply_markup']
        data['message_id'] = response.message_id
        user_message_data = {
            'data': data, 'params': params
        }

        await self.model.set_message(data=user_message_data)


@start_router.message(Command("start"))
async def start_user(message: types.Message, state: FSMContext):
    await state.set_state(state=UserStates.DELETE_MESSAGE)
    await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=message.chat.id))

    data, params = StartBuilder().build(
        message=message, message_id=message.message_id, text=ENG.INIT
    )

    model = models.users[message.chat.id]
    if await model.get_message_id():
        return await resend_bot_message(
            model=model, data=data, params=params
        )

    response = await bot.send_message(**data)
    saver = Saver(model)
    await saver.save_language()
    await saver.save_started_data(data=data, params=params, response=response)

    logger.info(f'Starting user {message.chat.id}')
