import asyncio
import time
from typing import Union
from uuid import UUID

from asyncpg import Connection, Pool, connect


# from config import host, username, password, database


async def create(conn: Union[Connection, Pool], clear=False) -> bool:
    """
    Создает таблицу users

    :param conn:    Объект подключения к БД
    :param clear:   If True -> очистить таблицу
    :return:
    """
    if clear:
        await conn.execute('DROP TABLE IF EXISTS users')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users(
            address             TEXT                    PRIMARY KEY,
            uid                 UUID                    NOT NULL
            txhash              TEXT                    NOT NULL            UNIQUE
        );
        ''')
    return True