import logging
import re

logger = logging.getLogger(__name__)


class MessageValidator:
    """
    Клас для валідації тексту повідомлення за шаблоном команди додавання акаунта.

    Використовує регулярний вираз для перевірки правильного формату команди
    /add_account або /add_account@BotName з тегом гравця.
    """

    _command_pattern = r'^/add_account(?:@TestCocTgBot)?\s#.*'

    def is_valid_message(
            self,
            message: str
    ) -> bool:
        """
        Перевірити чи повідомлення відповідає патерну команди додавання акаунта.

        :param message: Текст повідомлення, яке потрібно перевірити.
        :type message: str

        :return: True, якщо повідомлення валідне, інакше False.
        :rtype: bool
        """
        if re.fullmatch(self._command_pattern, message):
            return True
        return False


class Tag:
    """
    Клас для отримання тега гравця з тексту повідомлення.

    Використовує MessageValidator для перевірки правильності формату повідомлення перед отриманням тега.
    """
    def __init__(
            self
    ) -> None:
        """
        Ініціалізувати об'єкт Tag із вбудованим валідатором повідомлень.
        """
        self.validator = MessageValidator()

    def get_player_tag(
            self,
            message: str
    ) -> str | None:
        """
        Отримати тег гравця з повідомлення після валідації.

        :param message: Текст повідомлення користувача.
        :type message: str

        :return: Тег гравця без знаку '#' або None, якщо повідомлення невалідне.
        :rtype: str або None
        """
        if not self.validator.is_valid_message(message):
            return None

        tag = message.split(' ')[1]
        return tag
