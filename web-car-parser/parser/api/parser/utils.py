import logging
import re
import bs4
from curl_cffi import requests

logger = logging.getLogger(__name__)


class ListProcessor:
    def lists_to_dict(self, keys: list, values: list) -> dict:
        d = {}
        for i in range(len(keys)):
            d[keys[i]] = values[i]
        return d

    def length_is_equal(self, l1: list, l2: list) -> bool:
        if len(l1) == len(l2):
            return True
        return False

    def find_in_list(self):
        pass


class DataProcessor:
    def join_data(self, *args) -> dict:
        data = {}
        for item in args:
            key, value = list(item.keys())[0], list(item.values())[0]
            data[key] = value
        return data


class Requests:
    def get(self, url: str) -> str | None:
        response = requests.get(url=url, impersonate='chrome110')
        while response.status_code != 200:
            response = requests.get(url=url, impersonate='chrome110')
        try:
            return response.content.decode('windows-1250')
        except UnicodeDecodeError:
            logger.info(f'Returns "latin-1" encoding')
            return response.content.decode('latin-1')


class PageManager:
    _pagination_class = 'pagination'

    def get_current_page(self, url: str) -> str:
        return re.sub('.*stran=', '', url)

    def get_next_page(self, text: str, url: str, page: int) -> str:
        if not self.is_pagination_exist(text=text):
            logger.warning(f'Pagination class does not exist')
            return url
        return re.sub('stran=.*', f'stran={page}', url)

    def get_previous_page(self, url: str) -> str:
        page_data = re.search('stran=.*', url).group(0)
        current_page = page_data.split('=')[-1]
        if current_page != '2':
            return re.sub('stran=.*', f'stran={int(current_page) - 1}', url)
        return re.sub('stran=.*', f'stran=', url)

    def clear_page(self, url: str) -> str:
        logger.info(f'Clearing the page: {re.sub("stran=.*", "stran=", url)}')
        return re.sub('stran=.*', f'stran=', url)

    def is_pagination_exist(self, text):
        soup = bs4.BeautifulSoup(text, 'html.parser')
        return soup.find('ul', class_=self._pagination_class)
