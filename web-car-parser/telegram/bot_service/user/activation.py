import logging

from aiogram import F, types
from aiogram.fsm.context import FSMContext

from bot_service.user.main_menu import main_menu
from bot_service.user.utils.activation import Activation
from bot_service.user.utils.tasks import Notices, State
from shared.constructor.user import ActivateAccountBuilder
from shared.common.configs.bot import start_router, models, bot
from shared.common.states.user import UserStates
from shared.database.models import Admin
from shared.utils.date import Date
from shared.utils.localization import LanguageProcessor

logger = logging.getLogger(__name__)


@start_router.callback_query(F.data.startswith('activate_account'))
async def activate_account_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(state=UserStates.ACTIVATION)

    got_user_lang = callback.data.split(':')[-1]
    await models.users[callback.message.chat.id].set_language(data=got_user_lang)

    user_lang = LanguageProcessor.define_language(lang=got_user_lang)
    text = user_lang.ACTIVATION_PROCESS
    data, params = ActivateAccountBuilder().build(
        message=callback.message, message_id=callback.message.message_id, user_lang=user_lang, text=text
    )

    await bot.edit_message_text(**data)

    del data['reply_markup']
    await models.users[callback.message.chat.id].set_message(data={'data': data, 'params': params})


@start_router.message(UserStates.ACTIVATION)
async def activation_process(message: types.Message, state: FSMContext):
    model = models.users[message.chat.id]
    message_id = await model.get_message_id()
    tokens_data, user_lang = \
        await Admin(t_id=0).get_token_data(), await model.get_language()
    if tokens_data.get(message.text):
        await activate_user(
            message=message, state=state, message_id=message_id, tokens_data=tokens_data, user_lang=user_lang
        )
    else:
        await bad_activation(message=message, message_id=message_id, user_lang=user_lang)


async def activate_user(
        message: types.Message, state: FSMContext, message_id: int, tokens_data: dict, user_lang
):
    activation = Activation(message=message)

    await activation.success(state=state)
    date = Date.create_date(months=int(tokens_data.get(message.text)))

    await activation.activate(
        message_id=message_id, date=Date.transform_to_standard_date(date=date), user_lang=user_lang
    )

    await Notices.set_payment_reminder(message=message, date=date)
    await State.set_drop_user(message=message, user_lang=user_lang, date=date)

    logger.info(f'User {message.chat.id} was activated account')
    await main_menu(message=message, state=state)


async def bad_activation(message: types.Message, message_id: int, user_lang):
    text = user_lang.WRONG_TOKEN
    data, params = ActivateAccountBuilder().build(
        message=message, message_id=message.message_id, user_lang=user_lang, text=text
    )
    data['message_id'] = message_id
    await bot.edit_message_text(**data)
