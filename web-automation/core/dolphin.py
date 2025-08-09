import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Semaphore
import requests

from files import FileProcessor
from meta import Processor
from web import Ebay


class ThreadProcessor(Processor):
    """
    Менеджер управління потоками.
    
    Методи:
        - run_process(): Ініціалізація запуску потоків.
    """

    def __init__(self, count: int, data: list, params: dict):
        self.count = count
        self.semaphore = Semaphore(count)
        self.file_processor = FileProcessor()
        self.data = data
        self.params = params

    def run_process(self):
        """Ініціалізація роботи із потоками."""
        self.file_processor.create_log()
        with ThreadPoolExecutor(max_workers=self.count) as executor:
            for i, item in enumerate(self.data):
                executor.submit(self._run_task, item, i + 1)
                time.sleep(5)
        if threading.active_count():
            print('Програма закінчила свою роботу.')

    def _run_task(self, item: str, i: int):
        """Почерговий запуск потоків у Dolphin.
        
        :param item: Проксі (type: str).
        :param i: Номер потоку (type: int).
        """
        with self.semaphore:
            formatted_data = self.file_processor.change_format(data=item)
            dolphin = Dolphin(proxy=formatted_data, process_id=i, params=self.params)  # proxy=formatted_data
            email, password, cookies = dolphin.run_process()
            self.file_processor.add_data_to_log(process_id=i, email=email, password=password)
            if email:
                self.file_processor.create_cookie(email=email, content=cookies)
            else:
                sys.exit(0)


class Dolphin(Processor):
    """
    Клас для роботи із Dolphin Anty.

    Методи:
        - run_process(): Автоматизований ініціалізалізатор роботи.
    """
    token = '...'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru',
        'Referer': 'https://app.dolphin-anty-ru.online/',
        'Authorization': f'Bearer {token}'
    }

    def __init__(self, proxy: dict, process_id: int, params: dict):
        self.proxy = proxy
        self.process_id = process_id
        self.params = params
        self.lock = threading.Lock()

    def run_process(self) -> tuple:
        profile_id = self._create_profile()
        return self._run_profile(profile_id=profile_id)

    def _run_profile(self, profile_id) -> tuple:
        """
        Запуск профіля.

        :return: Повертає пошту та пароль (email, password).
        """
        with self.lock:
            url = f'http://localhost:3001/v1.0/browser_profiles/{profile_id}/start?automation=1'
            response = requests.get(url=url, headers=self.headers)
            if response.json().get('error'):
                print(f'Error: {response.json()}')
                self._delete_profile(profile_id=profile_id)
                return (None,)
        time.sleep(2)
        port = response.json()['automation']['port']

        web_params = {}
        for item in self.params.get('web'):
            for k, v in item.items():
                web_params[k] = v

        ebay = Ebay(
            process_id=self.process_id,
            port=port,
            email_type=web_params.get('emails'),
            cookies=web_params.get('cookies')
        )
        try:
            status = ebay.run_process()
            self._delete_profile(profile_id=profile_id)
            return status.get('email'), status.get('password'), status.get('cookies')
        except Exception:
            self._delete_profile(profile_id=profile_id)
            return None, None, None

    def _create_profile(self):
        """
        Створення профіля.

        :return: Повертає ID-профіля.
        """
        with self.lock:
            url = 'https://dolphin-anty-api.com/browser_profiles'
            data = self._generate_fingerprint(name=f'Profile {self.process_id}')
            response = requests.post(url=url, headers=self.headers, json=data)  # Need to handle error
            error = response.json().get('error')
            if error and error.get('type') == 'E_LIMIT':
                print('Ліміт створення профілів!')
                sys.exit(0)
            return response.json()['browserProfileId']

    def _get_cookies(self, profile_id):
        """ПОНОВИТИ МЕТОД ПІСЛЯ ПІДПИСКИ"""
        url = f'https://dolphin-anty-api.com/?actionType=getCookies&browserProfileId={profile_id}'
        data = {}
        requests.get(url=url, headers=self.headers, data=data)

    def _delete_profile(self, profile_id):
        """Видалення профіля."""
        url = f'https://dolphin-anty-api.com/browser_profiles/{profile_id}?forceDelete=1'
        requests.delete(url=url, headers=self.headers)

    def _generate_fingerprint(self, name: str):
        """
        Генерація відбитків для браузера.

        :return: Повертає список із відбитками (type: dict).
        """
        url = 'https://dolphin-anty-api.com/fingerprints/fingerprint?platform=windows&browser_type=anty' \
              '&browser_version=114&type=fingerprint&screen=1920x1080'
        response = requests.get(url=url, headers=self.headers)
        fingerprint = response.json()

        dolphin_params = {}
        for item in self.params.get('dolphin'):
            for k, v in item.items():
                dolphin_params[k] = v
        data = dict()
        data['name'] = name
        data['platform'] = dolphin_params.get('platform')
        data['browserType'] = 'anty'
        data['mainWebsite'] = 'none'

        data['useragent'] = {
            'mode': 'manual',
            'value': dolphin_params.get('useragent')
        }

        data['deviceName'] = {
            'mode': 'off',
            'value': None
        }

        data['macAddress'] = {
            'mode': 'off',
            'value': None
        }

        data['webrtc'] = {
            'mode': dolphin_params.get('webrtc'),
            'ipAddress': None
        }

        data['canvas'] = {
            'mode': dolphin_params.get('canvas')
        }

        data['webgl'] = {
            'mode': dolphin_params.get('webgl')
        }

        data['webglInfo'] = {
            'mode': 'manual',
            'vendor': fingerprint['webgl']['unmaskedVendor'],
            'renderer': fingerprint['webgl']['unmaskedRenderer'],
            'webgl2Maximum': fingerprint['webgl2Maximum']
        }

        data['webgpu'] = {
            'mode': 'manual'
        }

        data['clientRect'] = {
            'mode': dolphin_params.get('clientRect')
        }

        data['timezone'] = {
            'mode': 'auto',
            'value': None
        }

        data['locale'] = {
            'mode': 'auto',
            'value': None
        }

        data['proxy'] = self.proxy

        data['geolocation'] = {
            'mode': 'auto',
            'latitude': None,
            'longitude': None,
            'accuracy': None
        }

        data['cpu'] = {
            'mode': 'manual',
            'value': '8'
        }

        data['memory'] = {
            'mode': 'manual',
            'value': '8'
        }

        data['screen'] = {
            'mode': 'real',
            'resolution': None
        }

        data['audio'] = {
            'mode': 'real'
        }

        data['mediaDevices'] = {
            'mode': 'real',
            'audioInputs': None,
            'videoInputs': None,
            'audioOutputs': None
        }

        data['ports'] = {
            'mode': 'protect',
            'blacklist': '3389,5900,5800,7070,6568,5938'
        }

        data['doNotTrack'] = False
        data['args'] = []
        data['platformVersion'] = dolphin_params.get('platformVersion')
        data['uaFullVersion'] = dolphin_params.get('uaFullVersion')
        data['login'] = ''
        data['password'] = ''
        data['appCodeName'] = 'Mozilla'
        data['platformName'] = 'WindowsNT'
        data['connectionDownlink'] = fingerprint['connection']['downlink']
        data['connectionEffectiveType'] = fingerprint['connection']['effectiveType']
        data['connectionRtt'] = fingerprint['connection']['rtt']
        data['connectionSaveData'] = fingerprint['connection']['saveData']
        data['cpuArchitecture'] = fingerprint['cpu']['architecture']
        data['osVersion'] = dolphin_params.get('osVersion')
        data['vendorSub'] = ''
        data['productSub'] = fingerprint['productSub']
        data['vendor'] = fingerprint['vendor']
        data['product'] = fingerprint['product']

        return data
