import logging
from typing import List

from aiogram.types import Poll

from config.bot import PollConfig
from config.sheets import worksheet_title, Columns
from handlers.core.base import Processor

logger = logging.getLogger(__name__)


class PollProcessor(Processor):
    """
    Обробник відповідей на опитування у Google Sheets.

    Клас відповідає за обробку відповідей користувачів на опитування
    і збереження результатів у відповідну таблицю.

    :param title: Назва листа Google Sheets для збереження відповідей.
    :type title: str
    """

    def __init__(
        self,
        title: str = worksheet_title
    ) -> None:
        super().__init__(title=title)
        self.poll_config = PollConfig

    def process(
        self,
        index_answer: List[int]
    ) -> str:
        """
        Обробити вибрану відповідь із опитування.

        :param index_answer: Індекси вибраних відповідей користувачем.
        :type index_answer: List[int]

        :return: Текст вибраної відповіді або порожній рядок, якщо немає вибору.
        :rtype: str
        """
        return '' if not index_answer else self.poll_config.answers()[index_answer[0]]

    def save(
        self,
        poll_answer: Poll,
        user_answer: str,
    ) -> None:
        """
        Зберегти відповідь користувача на опитування у таблицю.

        Якщо користувача не знайдено у таблиці (немає зареєстрованого акаунта),
        відповідь не буде збережено.

        :param poll_answer: Об'єкт відповіді користувача на опитування.
        :type poll_answer: aiogram.types.PollAnswer
        :param user_answer: Вибрана відповідь користувача (текст).
        :type user_answer: str
        """
        user = self.get_records.get_record(val=poll_answer.user.id, col_name=Columns.USER_ID.value)
        if not user:
            logger.info(
                f'User {poll_answer.user.first_name} ({poll_answer.user.username}) tried to answer without account'
            )
            return
        user[Columns.ANSWER.value] = user_answer
        self.set_records.set_value(
            record=[[user_answer]],
            col_name=Columns.ANSWER.value,
            idx=user.get('Record ID')
        )
