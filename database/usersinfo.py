import asyncio
import time
from typing import Union

from asyncpg import Connection, Pool, connect


# from config import host, username, password, database


async def create(conn: Union[Connection, Pool], clear=False) -> bool:
    """
    Создает таблицу usersinfo

    :param conn:    Объект подключения к БД
    :param clear:   If True -> очистить таблицу
    :return:
    """
    if clear:
        await conn.execute('DROP TABLE IF EXISTS usersinfo')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS usersinfo(
            uuid                UUID        REFERENCES      users(uuid)
            info                TEXT        DEFAULT ''
        );
        ''')
    return True
