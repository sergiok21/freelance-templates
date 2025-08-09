import re

from kopeechka import Kopeechka
from sms_activate import SmsActivate
from twocaptcha import TwoCaptcha


class CheckBalance:
    """
    Отримання балансу з усіх сервісів.

    Методи:
        - get_balances(): Отримання балансу.
    """
    captcha_token = '...'

    def __init__(self):
        self.sms_activate = SmsActivate()
        self.kopeechka = Kopeechka()
        self.captcha = TwoCaptcha(self.captcha_token)

    def get_balances(self):
        return {
            'sms_activate': self.sms_activate.get_balance(),
            'kopeechka': self.kopeechka.get_balance(),
            'captcha': self.captcha.get_balance()
        }


class Config:
    _params = {
        'web': [
            {'emails': 'GMAIL.COM, GMX.COM', 'comment': '# Може містити значення через кому.'},
            {'cookies': 'FILE_NAME.txt', 'comment': '# Якщо не потрібні кукі, то ставити "-".'}
        ],
        'dolphin': [
            {'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/121.0.0.0 Safari/537.36', 'comment': '# Брати з Dolphin або в інтернеті.'},
            {'platform': 'windows', 'comment': '# Може містити: windows, linux та macos'},  # windows, linux, macos
            {'platformVersion': '10.0.0', 'comment': '# Для Windows 10: 10.0.0, Windows 11: 15.0.0, MacOS: 10.15.7.'},
            {'osVersion': '10'},  # Duplicate platformVersion
            {'uaFullVersion': '121.0.6141.1', 'comment': '# Версія браузера (дивитись в інтернеті).'},  # Browser version
            {'canvas': 'real', 'comment': '# Приймає "noise" або "real"'},  # noise
            {'webrtc': 'altered'},
            {'webgl': 'real', 'comment': '# Приймає "noise" або "real"'},
            {'clientRect': 'real', 'comment': '# Приймає "" або "" (краще залишити "real").'},
            {'macAddress': '11:84:F2:7E:30:07'}  # random
        ]
    }

    def create_config(self):
        with open('config.txt', 'w') as f:
            f.write(self._prepare_config())

    def _prepare_config(self):
        text = '# Файл конфігурації програми. Те, що починається з "#" - коментар.\n' \
               '# Конфігураційний файл містить параметри "web" та "dolphin".\n' \
               '# В параметрі "web" вказуються: email та cookies.\n' \
               '# Формат: email: [GMX.COM, GMAIL.COM] або GMAIL.COM, cookies: "FILE.TXT".\n' \
               '# В параметрі "dolphin" вказано усі можливі налаштування\n' \
               '# (для коректного їх введення можна звернутись за посиланням:\n' \
               '# https://documenter.getpostman.com/view/15402503/Tzm8Fb5f#585826b6-84c1-49d7-82c5-c48e7067a2a1\n#\n' \
               '# Обов\'зково:\n' \
               '# 1. В кінці кожного рядку крапку не ставити.\n' \
               '# 2. Якщо є декілька даних (наприклад, як в web -> emails, то ставимо через кому.\n' \
               '# 3. Деякі параметри можуть містити певні значення.\n' \
               '# Наприклад у "dolphin": "altered", "real", "noise" ' \
               '# та інші.\n\n' \
               '# Примітка. Ці коментарі можна прибрати для зручності редагування.\n\n'
        for key, value in self._params.items():
            text += f'{key}:\n'
            text += self._process_config(value)
        return text

    def _process_config(self, params: list):
        text = ''
        for item in params:
            text += f'{item.get("comment")}\n' if item.get('comment') else ''
            for key, value in item.items():
                if key != 'comment':
                    text += f'    - {key}: {value}\n'
        return text

    def get_params(self):
        with open('config.txt', 'r') as f:
            data = f.read().split('\n')
        result = {}
        for item in data:
            if item and item[0] != '#':  # Params
                if re.findall('^\s+', item):
                    param = re.sub(r'^\s+-\s', '', item)
                    key, value = param.split(': ')[0], param.split(': ')[1]
                    if key != 'useragent' and ', ' in value:
                        content = {key: value.split(', ')}
                    else:
                        content = {key: value}
                    result[str(list(result.keys())[-1])].append(content)
                elif item[-1] == ':':
                    key = item[:-1]
                    result[key] = []
        return result
