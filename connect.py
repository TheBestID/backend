from asyncpg import Connection, Pool, create_pool

from config import host, user, password, database, service_name, aws_access_key_id, aws_secret_access_key, endpoint_url


async def get_connection() -> Pool:
    return await create_pool(host=host, user=user, password=password, database=database, min_size=1, max_size=1)


async def get_pool() -> Pool:
    return await create_pool(host=host, user=user, password=password, database=database, min_size=1,
                             max_size=1)  # TODO: в продукт убрать ограничение


async def check_db() -> Connection:
    pass
