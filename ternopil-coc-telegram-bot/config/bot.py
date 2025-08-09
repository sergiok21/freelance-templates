import os
from enum import Enum

from config.logger import *

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import load_dotenv


# Load .env file
load_dotenv()

# Set dispatcher
dp = Dispatcher()

# Config bot
bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Base router for handling requests
router = Router()

# Group chat id for admins for commands (admins must be a list)
group_chat_id = os.getenv('GROUP_ID')
raw_admins = os.getenv('ADMINS')
admins = [int(admin.strip()) for admin in raw_admins.split(',')]


# Poll config
class PollConfig(Enum):
    """Конфігурація опитувальника"""
    QUESTION = 'Берете участь на ЛВК? (якщо не з усіх аккаунтів, то відповісти нижче, які саме будуть)'
    YES = '✅ Так'
    NO = '❌ Ні'

    @classmethod
    def answers(cls):
        """Клас-метод для отримання відповідей із змінних класу"""
        return [cls.YES.value, cls.NO.value]
