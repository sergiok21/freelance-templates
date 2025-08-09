import requests


class SmsActivate:
    """
    SMS ACTIVATE API.

    Методи:
        - get_balance(): Отримання балансу.
    """
    token = '...'

    def get_balance(self) -> str:
        """Перевірка балансу.
        :return: Кількість кошт на сервісі у типі str
        """
        url = f'...'
        response = requests.get(url=url)
        return response.text.split(':')[1]
