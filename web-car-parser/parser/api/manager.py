import logging
import os
import threading

import requests

from api.parser.models import UserObject, ThreadObject
from api.parser.parser import Parser
from api.parser.utils import PageManager

logger = logging.getLogger(__name__)


class UserManager:
    def __init__(self):
        self.user_model = UserObject()
        self.thread_model = ThreadObject()
        self.page_manager = PageManager()

    def is_user_exist_in_link(self, link: str):
        return bool(self.user_model.link.get(link))

    def find_duplicates(self, user_id: str, link: str):
        if self.user_model.user.get(user_id):
            if link in self.user_model.user[user_id]:
                logger.info(f'User {user_id} has duplicate link')
                return True
        if self.user_model.link.get(link):
            if user_id in self.user_model.link[link]:
                logger.info(f'Users could not add to link filter. Found duplicate')
                return True
        return False

    def create_user(self, user_id: str, link: str, name: str):
        if self.user_model.user.get(user_id):
            self.user_model.user[user_id].update({link: name})
            logger.info(f'Updating user {user_id}')
        else:
            self.user_model.user[user_id] = {link: name}
            logger.info(f'Creating user {user_id}')
        if self.user_model.link.get(link):
            self.user_model.link[link].append(user_id)
            logger.info(f'Updating link for user {user_id}')
        else:
            self.user_model.link[link] = [user_id]
            logger.info(f'Creating link for user {user_id}')

    def single_remove(self, user_id: str, link: str):
        logger.info(f'Removing one user object {user_id}')
        links = self.user_model.user.get(user_id)
        if links:
            if self.user_model.link.get(link) and user_id in self.user_model.link.get(link):
                self.user_model.link[link].remove(user_id)
            if link in links:
                del self.user_model.user[user_id][link]
        logger.info(f'All users after removing: {list(self.user_model.link.values())}')

    def multiple_remove(self, user_id: str):
        logger.info(f'Multiple removing user object {user_id}')
        links = self.user_model.user.get(user_id)
        if links:
            for user_link in links.keys():
                if user_id in self.user_model.link.get(user_link):
                    self.user_model.link[user_link].remove(user_id)


class ThreadManager(UserManager):
    def __init__(self):
        super().__init__()

    def start_thread(self, user_id: str, link: str, name: str):
        link = PageManager().clear_page(url=link)
        duplicates = self.find_duplicates(user_id=user_id, link=link)

        if not self.is_user_exist_in_link(link=link) and not duplicates:
            self.create_user(user_id=user_id, link=link, name=name)
            thread = threading.Thread(target=Parser(user_id=user_id, link=link).start, args=[], daemon=True)
            thread.start()
            logger.info(f'Starting thread {thread.ident}. All threads: {threading.enumerate()}')
            return thread.ident
        if not duplicates:
            self.create_user(user_id=user_id, link=link, name=name)
            logger.info(f'User {user_id} was added to an existing thread')

    def stop_thread(self, user_id: str, link: str = None):
        link = PageManager().clear_page(url=link)
        if link:
            self.single_remove(user_id=user_id, link=link)
        else:
            self.multiple_remove(user_id=user_id)
        self.user_model.clear_empties_all()


class RequestManager:
    def __init__(self):
        self.thread = ThreadManager()

    def manage(self, data: dict):
        token = os.environ.get('PARSER_TOKEN_SERVICE')

        if data.get('user_status'):
            user_id, status = data['user_status']['user_id'], data['user_status']['status']
        else:
            user_id, status = None, data['all']

        response = requests.get(
            url=f'{os.environ.get("WEB_URL")}/URL',
            headers={'Authorization': token, 'User-Id': str(user_id) if user_id else ''},
        )
        if response.status_code == 200:
            self._process(check_user=user_id, token=token, data=response.json(), status=status)

    def _process(self, check_user: str | bool, token: str, data: list, status: bool):
        for item in data:
            filter_id, user_id, link, name, user_status = \
                item.get('id'), item.get('user_id'), item.get('link'), item.get('name'), item.get('status')
            if status:
                if check_user:
                    self.thread.start_thread(user_id=str(user_id), link=link, name=name)
                    self._send_data(filter_id=filter_id, token=token, user_id=user_id, status=status)
                elif user_status:
                    self.thread.start_thread(user_id=str(user_id), link=link, name=name)
                    self._send_data(filter_id=filter_id, token=token, user_id=user_id, status=status)
            else:
                if user_status:
                    self.thread.stop_thread(user_id=str(user_id), link=link)
                    self._send_data(filter_id=filter_id, token=token, user_id=user_id, status=status)

    def _send_data(self, filter_id, token, user_id, status):
        response = requests.patch(
            url=f'{os.environ.get("WEB_URL")}/URL',
            headers={'Authorization': token, 'User-Id': str(user_id)},
            json={'status': status}
        )
        if response.status_code in [200, 201, 204]:
            logger.info(f'Thread was updated for user {user_id} with status {status}')
            return
        logger.error(f'Thread ID was not sent. Status code: {response.status_code}')
