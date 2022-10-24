from asyncpg import Connection, Pool, create_pool

from config import host, username, password, database


async def get_connection() -> Pool:
    return await create_pool(host=host, user=username, password=password, database=database, min_size=1, max_size=1)


async def get_pool() -> Pool:
    return await create_pool(host=host, user=username, password=password, database=database)


async def check_db() -> Connection:
    pass
