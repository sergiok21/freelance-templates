import logging

from aiogram import types, F

from shared.constructor.user import MenuBuilder, ChangeLanguageBuilder
from shared.common.configs.bot import profile_router, bot, models
from shared.utils.localization import LanguageProcessor

logger = logging.getLogger(__name__)


@profile_router.callback_query(F.data.startswith('change_language'))
async def change_language_callback(callback: types.CallbackQuery):
    user_lang = await check_request_to_update_language(callback=callback)
    text = user_lang.CHANGE_LANGUAGE_SECTION
    data, params = ChangeLanguageBuilder(button_column=2).build(
        message=callback.message, message_id=callback.message.message_id, user_lang=user_lang, text=text
    )
    await bot.edit_message_text(**data)


async def check_request_to_update_language(callback: types.CallbackQuery):
    request_to_update_lang = callback.data.split(':')
    if len(request_to_update_lang) > 1:
        return await update_language(callback=callback, user_lang=request_to_update_lang[-1])
    return await models.users[callback.message.chat.id].get_language()


async def update_language(callback: types.CallbackQuery, user_lang: str):
    user_lang_obj = LanguageProcessor.define_language(lang=user_lang)
    data, params = MenuBuilder().build(
        message=callback.message,
        message_id=callback.message.message_id,
        user_lang=user_lang_obj,
        text=user_lang_obj.MAIN_MENU_SECTION
    )

    del data['reply_markup']
    await models.users[callback.message.chat.id].set_message(data={'data': data, 'params': params})
    await models.users[callback.message.chat.id].set_language(data=user_lang)

    logger.info(f'User {callback.message.chat.id} was changed language on {user_lang}')

    return user_lang_obj
