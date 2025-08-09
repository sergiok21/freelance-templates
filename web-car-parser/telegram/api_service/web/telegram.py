import asyncio
import logging
import os

from aiogram.exceptions import TelegramForbiddenError

from .models import DataModel
from shared.common.configs.bot import bot
from shared.database.models import User

logger = logging.getLogger(__name__)
loop = asyncio.new_event_loop()


class Verifier:
    def check_user_id_and_token(self, header_user_id, header_token):
        if header_token == os.environ.get('PARSER_TOKEN_SERVICE'):
            return True
        return loop.run_until_complete(
            User(t_id=int(header_user_id)).is_token_exists(token=header_token)
        )


class Telegram:
    def send_message(self, user_id, instance: DataModel):
        name_and_link, price, description, telephones, location, user_link_and_name = \
            self._create_text(instance=instance)

        text = f'{name_and_link}' \
               f'{price}' \
               f'{description}' \
               f'{telephones}' \
               f'{location}' \
               f'{user_link_and_name}'

        try:
            loop.run_until_complete(bot.send_message(chat_id=user_id, text=text, disable_web_page_preview=True))
        except TelegramForbiddenError:
            logger.info(f'Message could not send cause user {user_id} disable bot')

    def _create_text(self, instance):
        name_and_link = f'<a href="{instance.link}"><b>{instance.name}</b></a>\n\n'
        price = f'Cena: {instance.price if instance.price else "-"}\n\n'
        description = '\n'.join(f'{k}: {v}' for k, v in instance.description.items()) + '\n\n' \
            if instance.description else ''
        telephones = 'Telefoni:\n' + '\n'.join(
            f'<a href="tel:{telephone}">{telephone}</a>' for telephone in instance.telephones
        ) + '\n\n'
        location = f'<a href="{instance.location.get("link")}">{instance.location.get("address")}</a>\n\n' \
            if instance.location else ''
        user_link_and_name = f'<i>Filter: <a href="{instance.user_link}">{instance.user_link_name}</a></i>'

        return name_and_link, price, description, telephones, location, user_link_and_name
