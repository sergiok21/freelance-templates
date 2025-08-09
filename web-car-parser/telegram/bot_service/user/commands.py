from aiogram.types import BotCommand, BotCommandScopeChat

from shared.common.configs.bot import bot


async def set_user_commands(chat_id: int, description: str):
    user_commands = [
        BotCommand(command="home", description=description),
    ]
    await bot.set_my_commands(commands=user_commands, scope=BotCommandScopeChat(chat_id=chat_id))
