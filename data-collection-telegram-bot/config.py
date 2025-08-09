from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

token = '...'

bot = Bot(token=token)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
