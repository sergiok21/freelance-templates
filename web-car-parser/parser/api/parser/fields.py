import logging
import re
import urllib.parse

from .utils import ListProcessor

logger = logging.getLogger(__name__)


class Name:
    def get_name(self, parent) -> dict | None:
        name_tag = parent.select_one('div span')
        if not name_tag:
            return {'name': None}
        return {'name': name_tag.text}


class Link:
    _site = '...'

    def get_detail_link(self, parent) -> dict | None:
        link = parent.find('a')
        if not link:
            return {'link': None}
        return {'link': self._site + re.sub(r'^\.\./', '', link['href'])}


class Price:
    _price_class = 'GO-Results-Price-TXT-Regular'
    _discount_price_class = 'GO-Results-Price-TXT-AkcijaCena'

    def get_price(self, parent) -> dict | None:
        price_tag = parent.find('div', class_=self._price_class)
        if not price_tag:
            price_tag = parent.find('div', class_=self._discount_price_class)
            if not price_tag:
                return {'price': None}
        try:
            return {'price': re.search(r'\d+.*\s€', price_tag.text).group(0)}
        except AttributeError:
            return {'price': None}


class Description:
    def __init__(self):
        self.list_processor = ListProcessor()

    def get_description(self, parent) -> dict | None:
        description_tag = parent.find_all('td')
        if not description_tag:
            return {'description': None}

        keys, values = self._get_keys_values(tag=description_tag)
        if not self.list_processor.length_is_equal(keys, values):
            return {'description': None}
        return {'description': self.list_processor.lists_to_dict(keys=keys, values=values)}

    def _get_keys_values(self, tag):
        keys, values = [], []
        for i, description_el in enumerate(tag):
            prepared_data = re.sub(r'^\s+|\r\n\s+', '', description_el.text)
            if i % 2 == 0:
                keys.append(prepared_data)
            else:
                values.append(prepared_data)
        return keys, values


class Location:
    _google_maps = 'https://www.google.com/maps/search/?api=1&query='

    def get_location(self, element) -> dict:
        try:
            location_tag = element.find('a', attrs={'data-target': '#MapModal'})
            if not location_tag:
                logger.info(f'Empty location cause location tag was not founded')
                return {'location': None}
            return self.process_location(location_tag.text)
        except AttributeError as ex:
            logger.info(f'Empty location cause raised Attribute Error: {ex}')
            return {'location': None}
        except UnicodeError:
            logger.info('Decode error while proceeding location')
            return {'location': None}

    def process_location(self, location) -> dict:
        address = re.search(r'\b.*\b', location).group(0)
        encoded_address = urllib.parse.quote(address)
        google_maps_url = f'{self._google_maps}{encoded_address}'
        logger.info(f'Location was successfully proceeded')
        return {'location': {'address': address, 'link': google_maps_url}}


class Telephone:
    def get_telephone(self, element) -> dict:
        try:
            telephones_tag = element.find_all('li')
            if not telephones_tag:
                logger.info(f'Empty telephones cause location tag was not founded')
                return {'telephones': None}
            return {'telephones': [self.process_telephone(telephone.text) for telephone in telephones_tag]}
        except AttributeError:
            telephones_tag = element.find('a', href=re.compile('tel:'))
            if not telephones_tag:
                logger.info(f'Empty telephones cause location tag was not founded in Attribute Error exception')
                return {'telephones': None}
            logger.info(f'Telephones was successfully proceeded')
            return {'telephones': [re.sub('tel:', '', telephones_tag['href'])]}
        except UnicodeError:
            logger.info('Decode error while proceeding telephones')
            return {'telephones': None}

    def process_telephone(self, telephone: str) -> str:
        telephone = re.search(r'\d+.*\s*\d+', telephone).group(0)
        return re.sub('\s|/|-', '', telephone)
