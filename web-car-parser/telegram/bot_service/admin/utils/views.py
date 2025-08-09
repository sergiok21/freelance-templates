import prettytable as pt
from aiogram import types

from shared.common.configs.bot import models
from shared.database.models import User
from shared.utils.date import Date


class TextProcessor:
    @staticmethod
    def new_line_text(text: str):
        mod = 0
        if len(text) % 2 != 0:
            mod += 1
        return f'{text[:int(len(text) / 2) + mod]}\n{text[int(len(text) / 2) + mod:]}'


class UsersSubscription:
    async def get_subscriptions(self, message: types.Message, from_=0, to_=1):
        table = pt.PrettyTable(['Тэг (Имя)', 'Дата'])

        users = []
        users_telegram_id = await models.admins[message.chat.id].get_users_telegram_id(from_=from_, to_=to_)

        for user in users_telegram_id:
            user_model = User(t_id=int(user))
            token_date = await user_model.get_token_date()
            if token_date:
                tag, first_name = \
                    await user_model.get_tag(), await user_model.get_first_name()
                tag = TextProcessor.new_line_text(text=tag) if len(tag) > 13 else tag
                first_name = TextProcessor.new_line_text(text=first_name) if len(first_name) > 13 else first_name
                text = f'{tag}\n({first_name})\n'
                users.append([text, token_date])
        return self._sort_table(table=table, users=users)

    def _sort_table(self, table, users):
        sort_users = Date.sort_date(users=users)
        for user in sort_users:
            table.add_row(tuple(user))
        return table
