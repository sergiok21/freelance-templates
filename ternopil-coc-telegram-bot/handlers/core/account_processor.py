import logging
from typing import Union, List, Dict

from aiogram.types import Message

from api.clash import ClashAPI
from config.sheets import worksheet_title, Columns
from handlers.core.base import Processor
from handlers.core.message_processor import Tag
from handlers.core.users import User

logger = logging.getLogger(__name__)


class AddAccountProcessor(Processor):
    """
    Обробник додавання акаунта користувача у Google Sheets.

    Цей клас обробляє процес додавання інформації про користувача та його акаунт
    Clash of Clans у таблицю Google Sheets.

    :param message: Повідомлення користувача, яке містить тег гравця.
    :type message: aiogram.types.Message
    :param title: Назва листа у Google Sheets (за замовчуванням використовується глобальне значення worksheet_title).
    :type title: str
    """
    def __init__(
            self,
            message: Message,
            title: str = worksheet_title
    ) -> None:
        super().__init__(title)

        self.message: Message = message
        self._player_info: dict
        self._record: list = []

    def process(
            self
    ) -> Dict[str, str | List[Union[int, float, str]]]:
        """
        Обробити повідомлення користувача і підготувати запис для вставки в таблицю.

        Перевіряє правильність тега гравця, отримує інформацію про акаунт через ClashAPI,
        формує запис для збереження.

        :return: Словник з ключем 'record' (готовий запис) або 'error' (текст помилки).
        :rtype: Dict[str, Union[str, List[int, float, str]]]
        """
        user_info = User.get_user_info(self.message)
        self._record.extend(user_info)
        logger.info(f'User info: {user_info}')

        tag = Tag().get_player_tag(self.message.text)
        if not tag:
            logger.info('Invalid tag.')
            return {
                'error': '❌ <b>Неправильно введено дані або неможливо перевірити тег.</b>\n\n'
                         '<i>Приклад: /add_account #YOUR_TAG</i>'
            }

        self._record.append(tag)
        logger.info(f'Player tag: {tag}')

        self._player_info = ClashAPI().get_player_info(tag)
        if not self._player_info or self._player_info.get('reason') == 'inMaintenance':
            logger.info('Failed to get player info.')
            return {
                'error': '❔ <b>Помилка із роботою API Clash of Clans.</b>\n\n'
                         '<i>Спробуйте здійснити запит пізніше.</i>'
            }

        self._record.append(self._player_info.get('name'))
        logger.info(f'Player info: {self._player_info.get("name")}')

        return {'record': self._record}

    def get_player_name(self) -> str:
        """
        Отримати ім'я гравця з ClashAPI після обробки.

        :return: Ім'я гравця.
        :rtype: str
        """
        return self._player_info.get('name')

    def save(
            self,
            record: List[Union[int, float, str]],
            col_name: str = None,
            idx: int = None
    ) -> None:
        """
        Зберегти підготовлений запис у таблицю.

        Якщо користувач вже існує у таблиці, то додає новий тег і ім'я гравця
        до існуючих даних.

        :param record: Список даних користувача для збереження.
        :type record: List[Union[int, float, str]]
        :param col_name: Назва колонки для пошуку користувача (наприклад, 'User ID').
        :type col_name: str
        :param idx: Індекс рядка у таблиці для оновлення (якщо потрібно).
        :type idx: int

        :raises ValueError: Якщо тег вже існує у записі користувача.
        """
        all_records = self.get_records.get_all_records()
        user = {}
        error = None

        for i, item in enumerate(all_records):
            if record[3] in item.get(Columns.PLAYER_TAG.value):
                error = ValueError(f'Tag {record[3]} exists in sheet')
            if record[0] == item.get(Columns.USER_ID.value):
                user = item
                idx = i + 1

        if error:
            raise error

        if user:
            user[Columns.PLAYER_TAG.value] = user[Columns.PLAYER_TAG.value] + f', {record[3]}'
            user[Columns.PLAYER_NAME.value] = user[Columns.PLAYER_NAME.value] + f', {record[4]}'
            record = list(user.values())

        self.set_records.set_value(record=[record], col_name=col_name, idx=idx)


class RemoveAccountProcessor(Processor):
    """TODO: Realize remove_account method"""

    def process(self):
        """TODO: IMPORTANT! Realize base method of Processor"""

    def save(self, *args, **kwargs):
        """TODO: IMPORTANT! Realize base method of Processor"""
