from typing import Union
from uuid import UUID
import time

from asyncpg import Connection, Pool



async def create(conn: Union[Connection, Pool], clear=False) -> bool:
    """
    Создает таблицу vacancy

    :param conn:    Объект подключения к БД
    :param clear:   If True -> очистить таблицу
    :return:
    """
    if clear:
        await conn.execute('DROP TABLE IF EXISTS vacancy')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS vacancy(
            id                  TEXT        PRIMARY KEY,
            owner_uuid          UUID        NOT NULL,
            price               INT         NOT NULL,
            category            TEXT        DEFAULT '',
            timestamp           TEXT        DEFAULT '',
            info                TEXT        NOT NULL
            
        );
        ''')
    return True

# what is the defualt type of timestamp?
async def add_vacancy(conn: Union[Connection, Pool], id: str, owner_uuid: UUID, price: int, category: str, timestamp: str, info: str):
    """
    """
    await conn.execute("""
        INSERT INTO vacancy (id, owner_uuid, price, category, timestamp, info)
        VALUES ($1, $2, $3, $4, $5, $6)
        """, id, owner_uuid, price, category, timestamp, info)



async def get_database(conn: Union[Connection, Pool]) -> list:
    """
    Возвращает бд

    :param conn:        Объект подключения к БД
    :return:
    """
    return await conn.fetch("""
        SELECT id, owner_uuid, price, category, timestamp, info
        FROM vacancy;
        """)


async def clear_database(conn: Union[Connection, Pool]):
    """

    :param conn:        Объект подключения к БД
    :return:
    """
    await conn.execute("""
        DELETE FROM vacancy;
        """)
    return