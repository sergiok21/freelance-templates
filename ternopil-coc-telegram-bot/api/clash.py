import json
import os
from typing import Dict, Union

import requests


class ClashAPI:
    """Клас для роботи з Clash of Clans API."""
    _base_url = 'https://api.clashofclans.com/v1/'

    def get_player_info(
            self,
            tag: str
    ) -> Dict[str, Union[int, float, str]] | None:
        """
        Отримати повну інформацію про гравця за його тегом.

        :param tag: Тег гравця у Clash of Clans (наприклад, '#ABC123').
        :type tag: str

        :return: Словник з даними гравця або None, якщо гравець не знайдений.
        :rtype: dict[str, int | float | str] або None
        """
        request_tag = tag.replace('#', '%23')

        player_url = f'players/{request_tag}'

        response = requests.get(
            url=f'{self._base_url}{player_url}',
            headers={'Authorization': f'Bearer {os.getenv("CLASH_TOKEN")}'}
        )

        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return None
