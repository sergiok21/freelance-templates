import logging

from aiogram import types, F

from shared.common.configs.bot import profile_router, bot, models
from shared.constructor.user import ProfileConfigurationBuilder

logger = logging.getLogger(__name__)


@profile_router.callback_query(F.data == 'profile_configuration')
async def profile_configuration_callback(callback: types.CallbackQuery):
    user_lang = await models.users[callback.message.chat.id].get_language()
    text = user_lang.PROFILE_SETTINGS_SECTION
    data, params = ProfileConfigurationBuilder().build(
        message=callback.message, message_id=callback.message.message_id, user_lang=user_lang, text=text
    )
    await bot.edit_message_text(**data)
