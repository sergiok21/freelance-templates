import logging

from aiogram.filters import Command
from aiogram.types import Message

from config.bot import router, bot
from handlers.core.account_processor import AddAccountProcessor

logger = logging.getLogger(__name__)


@router.message(Command('add_account'))
async def add_account(message: Message):
    """
    Обробник команди /add_account для додавання акаунта користувача у таблицю Google Sheets.

    Процес включає:
    - Відправку повідомлення про обробку запиту.
    - Валідацію та отримання інформації про акаунт через AddAccountProcessor.
    - Обробку можливих помилок (наприклад, неправильний тег або вже існуючий тег).
    - Збереження нового акаунта у таблиці.
    - Оновлення повідомлення з результатом виконання.

    :param message: Повідомлення користувача, що викликало команду.
    :type message: aiogram.types.Message

    :raises ValueError: Якщо тег гравця вже існує у таблиці.
    """
    logger.info(
        f'Adding account {message.from_user.id}.'
        f'Chat ID: {message.chat.id}. '
        f'Message: {message.text}'
    )

    response = await bot.send_message(
        chat_id=message.chat.id,
        text=f'📝 Обробляю запит...',
        reply_to_message_id=message.message_id
    )

    processor = AddAccountProcessor(message)
    record = processor.process()

    if record.get('error'):
        return await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=response.message_id,
            text=record.get('error')
        )

    logger.info(f'Output user data: {record}')

    try:
        processor.save(record=record.get('record'))
    except ValueError:
        return await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=response.message_id,
            text=f'❌ <b>Вказаний тег гравця вже доданий.</b>',
        )

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=response.message_id,
        text=f'✅ <b>Аккаунт {processor.get_player_name()} додано.</b>',
    )


@router.message(Command('remove_account'))
async def remove_account(message: Message):
    """TODO: Implement remove account (remove data from sheet; for example, user sold account)"""
