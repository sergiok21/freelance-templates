from typing import List, Dict, Union, Optional

from prettytable import PrettyTable

from api.sheets import GetRecords
from config.sheets import Columns


default_columns: List[str] = [
    '№',
    Columns.PLAYER_NAME.value,
]
"""
default_columns: Стандартний список, як приклад.
"""


class BaseTable:
    """
    Базовий клас для створення таблиці з використанням PrettyTable.

    :param fields: Список заголовків стовпців таблиці. Якщо не вказано — використовується default_columns.
    """
    def __init__(
            self,
            fields: Optional[List[str]] = None
    ) -> None:
        self.fields = fields if fields is not None else default_columns
        self.table = PrettyTable(fields)

    @staticmethod
    def prepare_data_from_sheet(
            data: List[Dict[str, Union[int, float, str]]],
            col_names: List[str],
    ) -> List[List[str]]:
        """
        Готує дані з Google Sheets або іншого джерела у форматі списку рядків для таблиці.

        :param data: Список словників, де кожен словник представляє один запис користувача.
        :param col_names: Список назв колонок, які потрібно включити у результат.
        :return: Список списків рядків (двовимірний список) для додавання у таблицю.
        """
        processed = []
        for i, item in enumerate(data, start=2):
            user_data = []
            for column in col_names:
                if not item.get(Columns.ANSWER.value):
                    user_data += [str(i)] + [item.get(column)]
            if user_data:
                processed.append(user_data)
        return processed


class TableBuilder(BaseTable):
    """
    Клас для побудови таблиці на основі підготовлених даних.

    Успадковується від BaseTable, щоб використовувати доступ до PrettyTable.
    """
    def add_rows(
            self,
            rows: List[List[str]]
    ) -> None:
        """
        Додає підготовлені рядки у таблицю.

        :param rows: Список рядків, де кожен рядок — список значень.
        """
        for row in rows:
            self.table.add_row(row)


class TableManager:
    """
    Відповідає за підготовку та вивід таблиці користувачів, які не відповіли на опитування.

    :param fields: Опціональний список заголовків для таблиці. Якщо не передано — використовується default_columns.
    """
    def __init__(
            self,
            fields: Optional[List[str]] = None
    ) -> None:
        self.table_builder = TableBuilder(fields if fields is not None else default_columns)
        self.get_records = GetRecords()

    def show_by_rows(self) -> PrettyTable:
        """
        Повертає PrettyTable із записами користувачів, які не відповіли на опитування.

        :return: Об'єкт PrettyTable із заповненими рядками.
        """
        records = self.get_records.get_all_records()
        prepared_data = self.table_builder.prepare_data_from_sheet(
            data=records,
            col_names=default_columns[1:]
        )
        self.table_builder.add_rows(prepared_data)
        return self.table_builder.table
