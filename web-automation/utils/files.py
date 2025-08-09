import json
import os
import threading


class FileProcessor:
    """
    Клас для обробки даних та файлів.

    Методи:
        - get_data(): Отримання даних з проксі-файлу.
        - change_format(data: str): Зміна формату даних (для Dolphin).
        - create_log(): Створення лог-файлу.
        - add_data_to_log(process_id, email=None, password=None): Додання інформації про стан роботи програми.
    """
    def __init__(self):
        self.lock = threading.Lock()

    def get_data(self, file: str) -> list:
        """
        Отримання даних з проксі-файлу.

        :return: Дані з файлу (type: list).
        """
        with open(file) as f:
            data = f.read().split()
        return data

    def change_format(self, data: str) -> dict:
        """
        Зміна формату даних.

        :param data: Дані з проксі-файлу.
        :type data: str
        :return: Повернення зміненого формату (type: dict).
        """
        split_data = data.split(':')
        return {'type': 'http',
                'name': 'proxy',
                'host': split_data[0],
                'port': split_data[1],
                'login': split_data[2],
                'password': split_data[3]}

    def create_log(self) -> None:
        """Створення лог-файлу."""
        with open('log.txt', 'w') as f:
            f.write('Успішно: 0, Безуспішно: 0\n\n')

    def add_data_to_log(self, process_id, email=None, password=None):
        """
        Додання інформації про стан роботи програми.

        :param process_id: Поточний поток програми.
        :type process_id: int | str
        :param email: Пошта з реєстрації аккаунту.
        :type email: None | str
        :param password: Пароль до аккаунту..
        :type password: None | str
        """
        with self.lock:
            with open('log.txt', 'r') as f:
                data = f.read().split('\n')
            split_first_line = data[0].split(',')
            successfully, unsuccessfully = split_first_line[0].split(': ')[-1], split_first_line[1].split(': ')[-1]
            log = f'Успішно: {int(successfully) + 1 if email else successfully}, ' \
                  f'Безуспішно: {int(unsuccessfully) + 1 if not email else unsuccessfully}'
            info = f'Поток {process_id}: {email}:{password}' if email else f'Поток {process_id}: -'
            data[0] = log
            data.append(info)
            with open('log.txt', 'w') as f:
                f.write('\n'.join(data))

    def create_cookie(self, email: str, content: list) -> None:
        if not os.path.exists('cookies'):
            os.mkdir('cookies')
        with open(f'cookies/{email}.txt', 'w') as f:
            f.write(json.dumps(content))
