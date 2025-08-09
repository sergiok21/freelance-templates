import logging

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot_service.user.commands import set_user_commands
from shared.constructor.user import MenuBuilder
from shared.utils.request import Sender, Request
from shared.common.configs.bot import models, bot_headers
from shared.common.states.user import UserStates, UpdateUser
from shared.database.models import Admin, Task

logger = logging.getLogger(__name__)


class Successful:
    def __init__(self, message: types.Message):
        self.message: Message = message

    async def success(self, state: FSMContext):
        job_id = await Admin(t_id=0).get_token_task(token=self.message.text)
        Task.delete(job_id=job_id)
        await Admin(t_id=0).delete_token_task(token=self.message.text)
        await Admin(t_id=0).delete_token(token=self.message.text)
        await state.set_state(state=UserStates.DELETE_MESSAGE)


class Activation(Successful):
    def __init__(self, message):
        super().__init__(message=message)

    async def activate(self, message_id, date, user_lang):
        data, params = MenuBuilder(button_column=1).build(
            message=self.message, message_id=message_id, user_lang=user_lang, text=user_lang.MAIN_MENU_SECTION
        )
        del data['reply_markup']

        await self._save_user_data(data=data, params=params, date=date)
        await set_user_commands(chat_id=self.message.chat.id, description=user_lang.TO_HOME_PAGE)

        logger.info(f'User {self.message.chat.id} was created account in web service')

    def _send_data_to_web(self):
        status = Sender.send_data_to_service(
            method=Request().post, headers=bot_headers,
            t_id=str(self.message.chat.id), token=self.message.text,
            is_superuser=False
        )
        if status == 400:
            patch_status = Sender.send_data_to_service(
                method=Request().patch, headers=bot_headers,
                t_id=str(self.message.chat.id), token=self.message.text
            )
            if patch_status != 204:
                UpdateUser.update_web_data(
                    headers=bot_headers, t_id=str(self.message.chat.id), token=self.message.text
                )
        else:
            UpdateUser.update_web_data(headers=bot_headers, t_id=str(self.message.chat.id), token=self.message.text)

    async def _save_user_data(self, data: dict, params: list, date: str):
        await models.users[self.message.chat.id].set_message(data={'data': data, 'params': params})
        await models.users[self.message.chat.id].set_token_data(data={self.message.text: date})
        await models.users[self.message.chat.id].create_bot()
        await models.users[self.message.chat.id].create_notices()

        self._send_data_to_web()


class Update(Successful):
    def __init__(self, message):
        super().__init__(message=message)

    async def update(self, current_token, date):
        await models.users[self.message.chat.id].set_token_data(data={self.message.text: date})

        headers = {
            'Authorization': str(current_token),
        }
        if not Sender.send_data_to_service(
                method=Request().patch, headers=headers, t_id=self.message.chat.id, token=self.message.text
        ):
            logger.warning(f'Creating or updating token could not proceed. '
                           f'Creating the worker task for sending token to web service')
            UpdateUser.update_web_data(
                headers=headers, t_id=str(self.message.chat.id), token=self.message.text
            )
            return
        logger.info(f'User {self.message.chat.id} was updated account in web service')
