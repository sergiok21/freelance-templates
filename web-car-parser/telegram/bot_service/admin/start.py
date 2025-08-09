import logging

from aiogram import types, F
from aiogram.fsm.context import FSMContext

from bot_service.admin.commands import set_admin_commands
from shared.constructor.admin import StartBuilder
from bot_service.admin.utils.validators import is_admin
from shared.common.configs.bot import bot, admin_router, models
from shared.utils.localization import ADMIN
from shared.common.states.admin import AdminStates

logger = logging.getLogger(__name__)


@admin_router.callback_query(F.data == 'admin_main_menu')
@is_admin
async def start_admin(callback: types.Message | types.CallbackQuery, state: FSMContext):
    if isinstance(callback, types.CallbackQuery):
        instance = callback.message
        message_id = callback.message.message_id
    else:
        instance = callback
        message_id = await models.admins[instance.chat.id].get_message_id()

    text = ADMIN.MAIN_MENU
    data, params = StartBuilder().build(message=instance, message_id=message_id, text=text)
    if not message_id:
        await state.set_state(state=AdminStates.DELETE_MESSAGE)
        await set_admin_commands(chat_id=instance.chat.id)

        response = await bot.send_message(**data)
        logger.info(response.message_id)
        del data['reply_markup']
        data['message_id'] = response.message_id

        await models.admins[instance.chat.id].set_message(data=data)
    else:
        data['message_id'] = message_id
        await bot.edit_message_text(**data)
    logger.info(f'Admin {instance.chat.id} in main menu')
