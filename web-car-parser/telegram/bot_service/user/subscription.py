import logging

from aiogram import types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from bot_service.user.utils.activation import Update
from bot_service.user.utils.tasks import State, Notices
from shared.constructor.user import SubscriptionBuilder, UpdateSubscriptionBuilder
from shared.common.states.user import UserStates
from shared.database.models import Admin
from shared.utils.date import Date
from shared.common.configs.bot import subscription_router, bot, models
from shared.utils.localization import BaseLanguage

logger = logging.getLogger(__name__)


@subscription_router.callback_query(F.data == 'subscriptions')
async def subscription_callback(message: types.CallbackQuery | types.Message, state: FSMContext, text=None):
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.set_state(UserStates.DELETE_MESSAGE)
    user_lang = await models.users[message.chat.id].get_language()
    message_id = await models.users[message.chat.id].get_message_id()
    expiration_token_date = await models.users[message.chat.id].get_token_date()
    text = f'{text if text else ""}' \
           f'{user_lang.EXPIRATION_DATE.format(expiration_token_date)}\n\n' \
           f'{user_lang.SUBSCRIPTION_SECTION}'

    data, params = SubscriptionBuilder(button_column=2).build(
        message=message, message_id=message_id, user_lang=user_lang, text=text
    )

    await bot.edit_message_text(**data)


@subscription_router.callback_query(F.data == 'update_subscription')
async def update_subscription_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.UPDATE_SUBSCRIPTION)

    user_lang = await models.users[callback.message.chat.id].get_language()
    text = f'{user_lang.UPDATE_SUBSCRIPTION_PROCESS}\n\n' \
           f'{user_lang.UPDATE_SUBSCRIPTION_SECTION}'

    data, params = UpdateSubscriptionBuilder(button_column=2).build(
        message=callback.message, message_id=callback.message.message_id, user_lang=user_lang, text=text
    )

    await bot.edit_message_text(**data)


@subscription_router.message(UserStates.UPDATE_SUBSCRIPTION)
async def process_update_subscription(message: types.Message, state: FSMContext):
    updates = Update(message=message)
    tokens_data, user_lang = await Admin(t_id=0).get_token_data(), await models.users[message.chat.id].get_language()
    if tokens_data.get(message.text):
        await success_update(
            message=message, state=state, updates=updates, tokens_data=tokens_data, user_lang=user_lang
        )
    else:
        await bad_update(message=message, user_lang=user_lang)


async def success_update(
        message: types.Message, state: FSMContext, updates: Update, tokens_data: dict, user_lang: BaseLanguage
):
    await updates.success(state=state)
    token = await models.users[message.chat.id].get_token_data()
    current_token, current_date = list(token.keys())[0], list(token.values())[0]
    update_date = Date.update_date(date=current_date, months=int(tokens_data.get(message.text)))
    update_reminder_date = Date.update_date(
        date=current_date, days=-3, months=int(tokens_data.get(message.text))
    )

    await updates.update(current_token=current_token, date=Date.transform_to_standard_date(date=update_date))
    await State.update_drop_user(message=message, user_lang=user_lang, date=update_date)

    if await models.users[message.chat.id].get_payment():
        await Notices.update_payment_reminder(message=message, date=update_reminder_date)
    logger.info(f'User {message.chat.id} was updated account')
    await subscription_callback(message=message, state=state, text=user_lang.SUBSCRIPTION_UPDATED)


async def bad_update(message: types.Message, user_lang: BaseLanguage):
    text = f'{user_lang.WRONG_TOKEN}\n\n' \
           f'{user_lang.UPDATE_SUBSCRIPTION_SECTION}\n\n'
    message_id = await models.users[message.chat.id].get_message_id()
    try:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text=text)
    except TelegramBadRequest:
        pass
