import random
import requests
from bs4 import BeautifulSoup


class Kopeechka:
    """Kopeechka API.

    Методи:
        - get_balance: Повертає баланс.
        - get_email(email_id): Замовляє пошту.
        - get_massage(email_id): Перевіряє та обробляє посилання.
        - delete_email(email_id): Видаляє пошту.
    """
    token = '...'

    def get_balance(self) -> str:
        """
        Отримати баланс Kopeechka.
        :return: Повертає баланс у типі str.
        """
        url = f'https://api.kopeechka.store/user-balance?token={self.token}&type=&TYPE&api=2.0'
        response = requests.get(url=url)
        return response.json()['balance']

    def get_email(self, email_type) -> tuple:
        """
        Отримати пошту.
        :return: Повертає пошту та ID у типі tuple (id, email).
        """
        # email_type = random.choice(['GMX.COM', 'GMAIL.COM'])

        url = f'https://api.kopeechka.store/mailbox-get-email?site=kleinanzeigen.de&mail_type=' \
              f'{email_type if type(email_type) == str else random.choice(email_type)}&token=' \
              f'{self.token}&password=$PASSWORD&regex=$REGEX&subject=$SUBJECT&investor=' \
              f'$INVESTOR&soft=$SOFT_ID&type=$TYPE&api=2.0'
        response = requests.get(url=url)
        return response.json()['id'], response.json()['mail']

    def get_message(self, email_id) -> str:
        """
        Отримати повідомлення з пошти.
        :param email_id: ID пошти.
        :type email_id: str or int.
        :return: Повертає пошту у типі dict (id, email).
        """
        url = f'https://api.kopeechka.store/mailbox-get-message?id={email_id}&token={self.token}&full=$FULL&type' \
              f'=$TYPE&api=2.0'
        response = requests.get(url=url)
        message = response.json().get('fullmessage')
        return self._process_message(message)

    def _process_message(self, message: str):
        """
        Обробка HTML-повідомлення.
        :param message: Повідомлення HTML-формату.
        :type message: str
        :return: Повертає посилання або повідомлення про результат обробки.
        """
        if message:
            soup = BeautifulSoup(message, 'html.parser')
            link = soup.find_all('a')[1].get('href')
            return link
        return ''

    def delete_email(self, email_id):
        """
        Видалити пошту.
        :param email_id: ID пошти.
        :type email_id: str | int
        """
        url = f'https://api.kopeechka.store/mailbox-cancel?id={email_id}&token={self.token}&type=$TYPE&api=2.0'
        requests.get(url=url)
