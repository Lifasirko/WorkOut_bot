import asyncio
from typing import Optional

import aioredis

from data import config

data_pool: Optional[aioredis.Redis] = None


async def create_pools():
    global data_pool
    data_pool = await aioredis.create_redis_pool(**config.redis, db=1)


asyncio.get_event_loop().run_until_complete(create_pools())

# class Database:
#     def __init__(self, pool):
#         self.pool: Pool = pool
#
#     @classmethod
#     async def create(cls):
#         pool = await asyncpg.create_pool(
#             user=config.PGUSER,
#             password=config.PGPASS,
#             host=config.IP
#         )
#         return cls(pool)
