from typing import Union

from asyncpg import Connection, Pool


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
            uuid                UUID        PRIMARY KEY,
            info                TEXT        DEFAULT ''
        );
        ''')
    return True


async def get_info(conn: Union[Connection, Pool], uuid: str) -> dict:
    """
    Возвращает бд

    :param conn:        Объект подключения к БД
    :param uuid:        soul_id
    :return:
    """
    return await conn.fetchrow("""
        SELECT info
        FROM usersinfo
        WHERE uuid = $1;
        """, uuid)


async def add_info(conn: Union[Connection, Pool], uuid: str, info: str):
    """
    Добавляет запись в таблицу usersinfo
    :param conn:
    :param uuid:
    :param info:
    :return:
    """
    await conn.execute("""
        INSERT INTO usersinfo (uuid, info)
        VALUES ($1, $2)
        """, uuid, info)
