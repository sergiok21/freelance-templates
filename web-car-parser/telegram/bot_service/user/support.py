from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from shared.constructor.user import SupportBuilder
from shared.common.configs.bot import profile_router, bot, models


@profile_router.callback_query(F.data == 'support')
async def support_callback(callback: CallbackQuery, state: FSMContext):
    user_lang = await models.users[callback.message.chat.id].get_language()
    text = user_lang.SUPPORT_SECTION
    data, params = SupportBuilder().build(
        message=callback.message, message_id=callback.message.message_id, user_lang=user_lang, text=text
    )

    await bot.edit_message_text(**data)
