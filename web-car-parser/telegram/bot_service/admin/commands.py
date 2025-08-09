from aiogram.types import BotCommand, BotCommandScopeChat

from shared.common.configs.bot import bot


async def set_admin_commands(chat_id: int):
    admin_commands = [
        BotCommand(command="home", description='На главную страницу'),
    ]
    return await bot.set_my_commands(commands=admin_commands, scope=BotCommandScopeChat(chat_id=chat_id))
