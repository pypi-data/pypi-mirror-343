import redis.asyncio as aredis

from typing import Protocol


class UndercurrRedis:
    def __init__(self, pool: aredis.ConnectionPool) -> None:
        self.redis_pool = pool
