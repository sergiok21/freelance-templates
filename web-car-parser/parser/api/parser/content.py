import logging
import re

import bs4

from .config import Locker
from .fields import Name, Link, Price, Description, Location, Telephone
from .models import UserObject
from .utils import Requests, PageManager, DataProcessor

logger = logging.getLogger(__name__)


class HTMLClasses:
    ad_class = 'row bg-white mb-3 pb-3 pb-sm-0 position-relative GO-Shadow-B GO-Results-Row'
    target_new_item_class = 'GO-ResultsRibbon'
    target_item_class = 'row bg-white position-relative GO-Results-Row GO-Shadow-B'
    target_price_class = 'GO-Results-Price-TXT-Regular'
    target_detail_class = 'col-12 col-lg-9 pb-2 border-left border-info'
    target_other_detail_class = 'row m-0 p-0 GO-Rounded'


class CSSStyles:
    target_item_style = 'z-index:1'


class AdContent(HTMLClasses):
    def get_ads(self, text: str):
        soup = bs4.BeautifulSoup(text, 'html.parser')
        return soup.find_all('div', class_=self.ad_class)


class PreviousContent(HTMLClasses, CSSStyles, DataProcessor, Name, Link, Price, Description):
    def get_previous_content(self, text):
        soup = bs4.BeautifulSoup(text, 'html.parser')
        return soup.find_all('div', class_=self.target_item_class, style=self.target_item_style)

    def find_content_until_equal_target_data(self, text, target_data):
        content = self.get_previous_content(text=text)
        previous_proceeded_content = []
        found_target_data = False
        for item in content:
            name, link, price, description = self.get_name(parent=item), self.get_detail_link(parent=item), \
                self.get_price(parent=item), self.get_description(parent=item)
            data = self.join_data(name, link, price, description)
            if data == target_data:
                found_target_data = True
                break
            previous_proceeded_content.append(data)
        if found_target_data:
            return previous_proceeded_content[::-1]
        return []


class ParentContent(HTMLClasses, CSSStyles):
    def __init__(self):
        self.requests = Requests()

    def get_parent_element(self, url: str):
        text = self.requests.get(url=url)
        soup = bs4.BeautifulSoup(text, 'html.parser')
        element = soup.find('div', class_=self.target_item_class, style=self.target_item_style)
        if not element:
            return None, text
        return element, text


class DetailContent(HTMLClasses, CSSStyles, Location, Telephone):
    def __init__(self):
        Location.__init__(self)
        Telephone.__init__(self)

        self.requests = Requests()

    def get_detail_element(self, url):
        text = self.requests.get(url=url)
        soup = bs4.BeautifulSoup(text, 'html.parser')
        element = soup.find('div', class_=self.target_detail_class)
        if not element:
            return soup.find('div', class_=self.target_other_detail_class)
        return element

    def get_detail_content(self, url):
        element = self.get_detail_element(url=url)
        if not element:
            logger.info('Detail element was not founded')
        telephones = self.get_telephone(element=element)
        logger.info(f'Telephones was proceeded')
        location = self.get_location(element=element)
        logger.info(f'Location was proceeded')
        logger.info(
            f'{f"Got location or telephones: {location}, {telephones}" if location or telephones else f"Location or telephones do not exist: {location}, {telephones}"}'
        )
        return location, telephones


class MainContent(AdContent, Name, Link, Price, Description):
    def __init__(self):
        Description.__init__(self)

        self.parent = ParentContent()
        self.page_manager = PageManager()
        self.lock = Locker()

    def get_main_content(self, url: str, parser_object):
        parent, text = self.parent.get_parent_element(url=url)
        parent, text, url = self.check_valid(parent=parent, text=text, url=url)
        parser_object.url, parser_object.text = url, text
        name, link, price, description = self.get_name(parent=parent), self.get_detail_link(parent=parent), \
            self.get_price(parent=parent), self.get_description(parent=parent)
        return name, link, price, description

    def check_valid(self, parent, text, url):
        if not parent:
            parent, text, url = self.recursive_get_main_content(url=url, text=text)
            logger.info(f'Updating page: {re.search("stran=.*", url).group(0) if re.search("stran=.*", url) else url}')
        elif not self.get_ads(text=text) and self.page_manager.get_current_page(url=url):
            previous_page = self.page_manager.get_previous_page(url=url)
            new_parent, new_text = self.parent.get_parent_element(url=previous_page)
            if parent:
                with self.lock:
                    UserObject().reset_key(new_key=previous_page, old_key=url)
                    parent, text, url = new_parent, new_text, previous_page
                    logger.info(f'Redirect to previous page: {url}')
        return parent, text, url

    def recursive_get_main_content(self, url: str, text: str, page: int = 2):
        url = self.page_manager.get_next_page(url=url, text=text, page=page)
        parent, text = self.parent.get_parent_element(url=url)
        if parent:
            return parent, text, url
        else:
            return self.recursive_get_main_content(url=url, text=text, page=page + 1)
