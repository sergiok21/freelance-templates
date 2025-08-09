import logging
import os

import requests

logger = logging.getLogger(__name__)


class Request:
    web_api_url = f'{os.environ.get("WEB_URL")}/api/user/'

    def post(self, headers: dict, url: str = web_api_url, **kwargs):
        return requests.post(url=url, headers=headers, json=kwargs)

    def patch(self, headers: dict, url: str = web_api_url, **kwargs):
        return requests.patch(url=url, headers=headers, json=kwargs)

    def delete(self, headers: dict, url: str = web_api_url, **kwargs):
        return requests.delete(url=url, headers=headers, json=kwargs)


class Sender:
    @staticmethod
    def send_data_to_service(
            method: callable,
            **kwargs
    ) -> int:
        try:
            response = method(**kwargs)
            return response.status_code
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout) as e:
            logger.critical(f'Data was not sent to service. Error: {str(e)} ')
            return 0
