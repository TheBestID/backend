from typing import Union
from uuid import UUID

from asyncpg import Connection, Pool


# from config import host, username, password, database


async def create_table_achievements(conn: Union[Connection, Pool], clear=False) -> bool:
    """
    Создает таблицу users
    :param conn:    Объект подключения к БД
    :param clear:   If True -> очистить таблицу
    :return:
    """
    if clear:
        await conn.execute('DROP TABLE IF EXISTS achievements')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS achievements(
            sbt_id              UUID        PRIMARY KEY,
            from                UUID        NOT NULL,
            to                  UUID        NOT NULL,
            cid                 TEXT        NOT NULL,
            type                TEXT        NOT NULL
        );
        ''')
    return True


async def get_table_achievements(conn: Connection):
    return await conn.fetch("""
        SELECT *
        FROM achievements;
        """)


async def add_achievements(conn: Union[Connection, Pool], sbt_id: UUID, _from: UUID, to: UUID, cid: str, _type: str):
    """
    :param conn:
    :param sbt_id:
    :param _from:
    :param to:
    :param cid:
    :param _type:
    :return:
    """
    await conn.execute("""
        INSERT INTO achievements (sbt_id, _from, to, cid, _type)
        VALUES ($1, $2, $3, $4, $5)
        """, sbt_id, _from, to, cid, _type)
