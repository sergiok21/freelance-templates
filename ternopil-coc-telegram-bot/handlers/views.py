import logging

from aiogram.filters import Command
from aiogram.types import Message

from config.bot import router, bot
from handlers.core.bot_table import TableManager

logger = logging.getLogger(__name__)


@router.message(Command('empty_answers'))
async def table_empty_answers_command(message: Message):
    table_view = TableManager()
    table = table_view.show_by_rows()

    await bot.send_message(chat_id=message.chat.id, text=f'<pre>{table.get_string()}</pre>')
