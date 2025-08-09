import logging

from aiogram.filters import Command
from aiogram.types import Message, Poll

from config.bot import router, bot, PollConfig, admins
from handlers.core.poll_processor import PollProcessor

logger = logging.getLogger(__name__)


@router.message(Command('create_poll'))
async def create_poll(message: Message):
    """
    Обробник команди /create_poll для створення нового опитування у групі.

    Процес включає:
    - Перевірку, чи користувач є адміністратором.
    - Створення опитування із заданим питанням і варіантами відповідей.
    - Закріплення повідомлення з опитуванням у чаті.

    :param message: Повідомлення користувача, що викликало команду.
    :type message: aiogram.types.Message

    :return: None
    """
    if message.from_user.id not in admins:
        logger.info(f'User {message.from_user.first_name} ({message.from_user.username}) tried to create a poll')
        return

    logger.info('Creating poll...')

    response = await bot.send_poll(
        chat_id=message.chat.id,
        question=PollConfig.QUESTION.value,
        options=PollConfig.answers(),
        is_anonymous=False
    )

    await bot.pin_chat_message(
        chat_id=message.chat.id,
        message_id=response.message_id
    )

    logger.info(f'Poll response: {response.message_id}')


@router.poll_answer()
async def handle_poll_answer(poll_answer: Poll):
    """
    Обробник відповіді користувача на опитування.

    Процес включає:
    - Отримання ID користувача та його вибраних варіантів.
    - Обробку вибраної відповіді через PollProcessor.
    - Збереження відповіді у таблицю Google Sheets.

    :param poll_answer: Відповідь користувача на опитування.
    :type poll_answer: aiogram.types.PollAnswer

    :return: None
    """
    user_id = poll_answer.user.id
    option_ids = poll_answer.option_ids
    logger.info(f'User answered: {user_id}. Poll options: {option_ids}')

    poll_processor = PollProcessor()
    answer = poll_processor.process(index_answer=option_ids)
    poll_processor.save(poll_answer=poll_answer, user_answer=answer)

    logger.info(f'User data {poll_answer.user.first_name} ({poll_answer.user.username}) saved!')
