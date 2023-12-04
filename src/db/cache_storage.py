from fastapi import Depends
from redis import Redis

from db.redis import get_redis

CACHE_EXPIRE_IN_SECONDS = 5 * 60


class RedisCacheStorage:
    def __init__(self, connection):
        self.connection: Redis = connection

    async def get_from_cache(self, key: str) -> str | None:
        data = await self.connection.get(key)
        if not data:
            return None
        return data

    async def put_to_cache(self, key: str, value: str, ttl: int) -> None:
        await self.connection.set(
            key, value,
            CACHE_EXPIRE_IN_SECONDS)

    async def del_from_cache(self, key: str) -> None:
        await self.connection.delete(key)


def get_cache_storage(connection=Depends(get_redis)):
    return RedisCacheStorage(connection)
