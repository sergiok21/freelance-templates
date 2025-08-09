import logging

from aiogram import types, F

from aiogram.fsm.context import FSMContext

from shared.common.states.user import UserStates
from shared.common.configs.bot import home_router, bot, models
from shared.constructor.user import MenuBuilder

logger = logging.getLogger(__name__)


@home_router.callback_query(F.data == 'main_menu')
async def main_menu(message: types.CallbackQuery | types.Message, state: FSMContext = None, text: str = None):
    instance = message.message if isinstance(message, types.CallbackQuery) else message

    if await state.get_state() != UserStates.DELETE_MESSAGE:
        await state.set_state(UserStates.DELETE_MESSAGE)

    user_lang = await models.users[instance.chat.id].get_language()
    message_id = await models.users[instance.chat.id].get_message_id()
    text = user_lang.MAIN_MENU_SECTION if not text else text

    data, params = MenuBuilder(button_column=1).build(
        message=instance, message_id=message_id, user_lang=user_lang, text=text
    )

    await bot.edit_message_text(**data)

    logger.info(f'User {instance.chat.id} was appeared to main menu')
