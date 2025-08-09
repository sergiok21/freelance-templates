from typing import List, Union

from aiogram.types import Message


class User:
    """
    Клас для отримання інформації про користувача з повідомлення Telegram.

    Містить утилітарний метод для збору базових даних користувача.
    """

    @staticmethod
    def get_user_info(message: Message) -> List[Union[int, float, str]]:
        """
        Отримати основну інформацію про користувача з повідомлення.

        Повертає список із трьома елементами:
        - ID користувача
        - Ім'я користувача
        - Telegram username користувача (або порожній рядок, якщо відсутній)

        :param message: Об'єкт повідомлення Telegram (aiogram.types.Message).
        :type message: Message

        :return: Список із ID, імені та тега користувача.
        :rtype: List[Union[int, float, str]]
        """
        user_id = message.from_user.id
        name = message.from_user.first_name
        tag = message.from_user.username if message.from_user.username else ''
        return [user_id, name, tag]
