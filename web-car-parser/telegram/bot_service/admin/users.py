from aiogram import F, types

from shared.constructor.admin import UsersViewBuilder
from bot_service.admin.utils.views import UsersSubscription
from shared.common.configs.bot import admin_router, bot, models
from shared.utils.localization import ADMIN


@admin_router.callback_query(F.data.startswith('show_users'))
async def show_users_callback(callback: types.CallbackQuery):
    to_ = int(callback.data.split(':')[-1])
    from_ = to_ - 5
    table = await UsersSubscription().get_subscriptions(message=callback.message, from_=from_, to_=to_)
    text = ADMIN.USERS_SUBSCRIPTION_INFO.format(table)
    users_id = await models.admins[callback.message.chat.id].get_users_telegram_id(from_=from_, to_=to_ + 1)
    data, params = UsersViewBuilder().build(
        message=callback.message, message_id=callback.message.message_id,
        text=text, from_=from_, to_=to_, users_id=users_id
    )

    await bot.edit_message_text(**data)
