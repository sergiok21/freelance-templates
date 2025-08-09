from aiogram.types import BotCommand, BotCommandScopeChatMember, BotCommandScopeDefault

from config.bot import bot, group_chat_id, admins


base_commands = [
    BotCommand(command="add_account", description='Додати аккаунт'),
]
"""
Базові команди, доступні всім користувачам.

- /add_account: Додати новий акаунт користувача.
"""

privilege_commands = [
    BotCommand(command='create_poll', description='Створити опитування'),
    BotCommand(command='empty_answers', description='Відобразити порожні відповіді із Google Sheets'),
]
"""
Додаткові команди для привілейованих користувачів (адміністраторів).

- /create_poll: Створити нове опитування у чаті.
- /answers: Відобразити відповіді із Google Sheets
"""


async def set_user_commands() -> None:
    """
    Встановити базові команди для всіх користувачів бота.

    Використовує BotCommandScopeDefault для налаштування доступних команд
    у приватних чатах та групах без персоналізованих налаштувань.

    :return: None
    """
    await bot.set_my_commands(
        commands=base_commands,
        scope=BotCommandScopeDefault()
    )


async def set_admin_commands() -> None:
    """
    Встановити розширений набір команд для адміністраторів у певному груповому чаті.

    Кожному адміністратору окремо задається список команд, який об'єднує базові та привілейовані команди.

    :return: None
    """
    admin_commands = base_commands + privilege_commands

    for admin_id in admins:
        await bot.set_my_commands(
            commands=admin_commands,
            scope=BotCommandScopeChatMember(chat_id=group_chat_id, user_id=admin_id)
        )
