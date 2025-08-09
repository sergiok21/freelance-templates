import logging
import os

import requests

logger = logging.getLogger(__name__)


class Telegram:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.token = os.environ.get('PARSER_TOKEN_SERVICE')

    def send_data(self, data) -> None:
        headers = {
            'Authorization': self.token,
            'User-Id': self.user_id,
        }
        requests.post(f'{os.environ.get("TELEGRAM_URL")}/URL', headers=headers, json=data)
