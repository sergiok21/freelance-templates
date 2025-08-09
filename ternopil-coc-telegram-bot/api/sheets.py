import logging
from typing import List, Dict, Union

import gspread
from gspread import Spreadsheet, Worksheet

from config.sheets import config, worksheet_title, Columns

logger = logging.getLogger(__name__)


class PrepareSheet:
    """
    Клас для створення або отримання листа (worksheet) у Google Sheets.

    :param sheet: Об'єкт Spreadsheet для роботи з таблицею.
    :type sheet: Spreadsheet
    """

    def __init__(self, sheet: Spreadsheet):
        self.sheet = sheet

    def get_or_create_worksheet(
            self,
            title: str = worksheet_title,
            rows: int = 100,
            cols: int = 5
    ) -> Worksheet:
        """
        Отримати існуючий лист або створити новий із заданими параметрами.

        :param title: Назва листа.
        :type title: str
        :param rows: Кількість рядків у листі (за замовчуванням 100).
        :type rows: int
        :param cols: Кількість колонок у листі (за замовчуванням 5).
        :type cols: int

        :return: Об'єкт Worksheet.
        :rtype: Worksheet
        """
        try:
            worksheet = self.sheet.add_worksheet(title=title, rows=rows, cols=cols)
            column_values = [
                [col.value for col in Columns]
            ]
            worksheet.update(column_values)
        except gspread.exceptions.APIError:
            worksheet = self.sheet.worksheet(title)
        return worksheet


class ValidateSheet:
    """
    Клас для валідації даних у листі.

    :param worksheet: Об'єкт Worksheet для перевірки даних.
    :type worksheet: Worksheet
    """

    def __init__(self, worksheet: Worksheet):
        self.worksheet = worksheet

    def validate_column_name(
            self,
            records: List[Dict[str, Union[int, float, str]]],
            col_name: str
    ) -> bool:
        """
        Перевірити чи існує вказана колонка в записах.

        :param records: Список записів.
        :type records: List[Dict[str, Union[int, float, str]]]
        :param col_name: Назва колонки для перевірки.
        :type col_name: str

        :return: True, якщо колонка існує, інакше False.
        :rtype: bool
        """
        if not records:
            return False
        return bool(records[0].get(col_name))


class Sheet:
    """
    Базовий клас для роботи з листом у Google Sheets.

    :param title: Назва листа.
    :type title: str
    """
    def __init__(
            self,
            title: str = worksheet_title
    ) -> None:
        sheet = config()
        self.worksheet = PrepareSheet(sheet).get_or_create_worksheet(title)
        self.validator = ValidateSheet(self.worksheet)


class GetRecords(Sheet):
    """
    Клас для отримання записів із листа.
    """

    def get_all_records(
        self
    ) -> List[Dict[str, Union[int, float, str]]]:
        """
        Отримати всі записи з листа.

        :return: Список усіх записів.
        :rtype: List[Dict[str, Union[int, float, str]]]
        """
        return self.worksheet.get_all_records()

    def get_record(
        self,
        idx: int = None,
        col_name: str = None,
        val: Union[int, float, str] = None
    ) -> Dict[str, Union[int, float, str]] | None:
        """
        Отримати запис за індексом або за значенням у колонці.

        :param idx: Індекс запису.
        :type idx: int
        :param col_name: Назва колонки для пошуку.
        :type col_name: str
        :param val: Значення для пошуку у вказаній колонці.
        :type val: int, float або str

        :return: Знайдений запис або None.
        :rtype: Dict[str, Union[int, float, str]] або None
        """
        if idx is not None:
            return self._get_by_id(idx)
        if col_name is not None and val is not None:
            return self._get_by_column_and_value(col_name, val)

        raise ValueError("idx or col_name was missed")

    def _get_by_id(
            self,
            idx: int
    ) -> Dict[str, Union[int, float, str]] | None:
        records = self.get_all_records()
        try:
            return records[idx]
        except IndexError:
            logger.info(f'Index {idx} out of range')
            return None

    def _get_by_column_and_value(
        self,
        col_name: str,
        val: Union[int, float, str]
    ) -> Dict[str, Union[int, float, str]] | None:
        records = self.get_all_records()

        if not self.validator.validate_column_name(records=records, col_name=col_name):
            logger.info('Records is empty!')
            return None

        for idx, record in enumerate(records):
            if record.get(col_name) == val:
                record['Record ID'] = idx
                return record
        else:
            logger.info(f"Record {col_name}={val} does not exists")
            return None


class SetRecords(Sheet):
    """
    Клас для встановлення (додавання або оновлення) записів у листі.

    :param title: Назва листа.
    :type title: str
    """

    def set_value(
        self,
        record: List[List[Union[int, float, str]]],
        idx: int = None,
        col_name: str = None
    ) -> None:
        """
        Додати новий рядок або оновити клітинку в листі.

        :param record: Дані для вставки або оновлення.
        :type record: List[List[Union[int, float, str]]]
        :param idx: Індекс рядка для оновлення.
        :type idx: int
        :param col_name: Назва колонки для оновлення.
        :type col_name: str
        """
        if col_name is None:
            self._add_row(record, idx)
        else:
            self._update_cell(record, col_name, idx)

    def _add_row(
            self,
            record: List[List[Union[int, float, str]]],
            idx: int = None
    ) -> None:
        """
        Додати новий рядок у лист.

        :param record: Дані для вставки.
        :type record: List[List[Union[int, float, str]]]
        :param idx: Індекс, куди вставити дані. Якщо не задано — вставка в кінець.
        :type idx: int
        """
        if not isinstance(record, list):
            raise ValueError("Record must be a list (list(list(...)).")

        if idx is None:
            values = self.worksheet.get_all_values()
            idx = len(values)

        self.worksheet.update(record, range_name=f'A{idx + 1}')

    def _update_cell(
            self,
            record: List[List[Union[int, float, str]]],
            col_name: str,
            idx: int
    ) -> None:
        """
        Оновити конкретну клітинку у листі.

        :param record: Дані для оновлення клітинки (у форматі списку списків).
        :type record: List[List[Union[int, float, str]]]
        :param col_name: Назва колонки, де оновлюється значення.
        :type col_name: str
        :param idx: Індекс рядка для оновлення.
        :type idx: int
        """
        if idx is None:
            raise ValueError("idx was missing.")

        headers = self.worksheet.row_values(1)
        try:
            col_idx = headers.index(col_name) + 1
        except ValueError:
            raise Exception(f"Column '{col_name}' does not exists.")

        cell = gspread.utils.rowcol_to_a1(idx + 2, col_idx)
        self.worksheet.update(record, range_name=cell)
