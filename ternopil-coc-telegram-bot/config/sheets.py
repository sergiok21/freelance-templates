import os
from enum import Enum

import gspread
from gspread import Spreadsheet

from google.oauth2.service_account import Credentials


worksheet_title = 'Users'  # or set your title


class Columns(Enum):
    """
    Перелік назв колонок для роботи з Google Sheets.

    Значення:
        USER_ID (str): Ідентифікатор користувача.
        NAME (str): Ім'я користувача.
        TELEGRAM_TAG (str): Telegram username користувача.
        PLAYER_TAG (str): Тег гравця в грі.
        PLAYER_NAME (str): Ім'я гравця в грі.
        ANSWER (str): Відповідь користувача на опитування.
    """
    USER_ID = 'User ID'
    NAME = 'Name'
    TELEGRAM_TAG = 'Telegram Tag'
    PLAYER_TAG = 'Player Tag(-s)'
    PLAYER_NAME = 'Player Name(-s)'
    ANSWER = 'Answer'


def config() -> Spreadsheet:
    """
    Ініціалізувати підключення до Google Sheets за допомогою облікових даних сервісного аккаунту.

    Використовує змінні середовища:
        - SHEET_CREDENTIALS: шлях до JSON-файлу з обліковими даними сервісного аккаунту.
        - SHEET_URL: URL-адреса таблиці Google Sheets.

    :return: Об'єкт Spreadsheet для роботи з таблицею.
    :rtype: Spreadsheet

    :raises FileNotFoundError: Якщо файл облікових даних не знайдено.
    :raises gspread.exceptions.SpreadsheetNotFound: Якщо таблицю за вказаною URL-адресою не знайдено.
    """
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = Credentials.from_service_account_file(
        os.getenv('SHEET_CREDENTIALS'), scopes=scopes
    )
    client = gspread.authorize(credentials)
    sheet_url = os.getenv("SHEET_URL")
    return client.open_by_url(sheet_url)
