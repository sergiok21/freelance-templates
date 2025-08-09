from redis.commands.json.path import Path

from shared.common.configs.redis import redis


class Redis:
    @staticmethod
    async def get(key, path=None):
        try:
            data = redis.json().get(key)
            if path:
                split_keys = path.split('.')
                for key in split_keys:
                    if key:
                        data = data.get(key)
            return data
        except AttributeError:
            return None

    @staticmethod
    async def set(key, data: dict | list | int | str, path=None):
        redis.json().set(key, path='.' if not path else Path(path), obj=data)

    @staticmethod
    async def delete(key, path):
        redis.json().delete(key, path=path)
