from abc import abstractmethod

from api.sheets import GetRecords, SetRecords
from config.sheets import worksheet_title


class Processor:
    """
    Абстрактний базовий клас для обробки даних у Google Sheets.

    Визначає інтерфейс для обробників, які повинні реалізовувати методи
    обробки даних (process) та їхнього збереження (save).

    :param title: Назва листа Google Sheets для обробки даних.
    :type title: str
    """

    def __init__(self, title: str = worksheet_title):
        self.get_records = GetRecords(title=title)
        self.set_records = SetRecords(title=title)

    @abstractmethod
    def process(self, *args, **kwargs):
        """
        Абстрактний метод для обробки даних.

        Повинен бути реалізований у підкласах для обробки вхідних даних перед збереженням.

        :param args: Додаткові позиційні аргументи для обробки.
        :param kwargs: Додаткові іменовані аргументи для обробки.
        :raises NotImplementedError: Якщо метод не реалізовано у підкласі.
        """
        pass

    @abstractmethod
    def save(self, *args, **kwargs):
        """
        Абстрактний метод для збереження оброблених даних у Google Sheets.

        Повинен бути реалізований у підкласах для збереження даних після обробки.

        :param args: Додаткові позиційні аргументи для збереження.
        :param kwargs: Додаткові іменовані аргументи для збереження.
        :raises NotImplementedError: Якщо метод не реалізовано у підкласі.
        """
        pass
