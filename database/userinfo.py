from typing import Union

from asyncpg import Connection, Pool


# from config import host, username, password, database


async def create_table_userinfo(conn: Union[Connection, Pool], clear=False) -> bool:
    """
    Создает таблицу userinfo

    :param conn:    Объект подключения к БД
    :param clear:   If True -> очистить таблицу
    :return:
    """
    if clear:
        await conn.execute('DROP TABLE IF EXISTS userinfo')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS userinfo(
            uuid                UUID        PRIMARY KEY,
            username            TEXT        DEFAULT '',
            info                TEXT        DEFAULT ''
        );
        ''')
    return True


async def get_info(conn: Union[Connection, Pool], uuid: str) -> dict:
    """
    :param conn:
    :param uuid:
    :return:
    """
    return await conn.fetchrow("""
        SELECT info
        FROM userinfo
        WHERE uuid = $1;
        """, uuid)


async def add_info(conn: Union[Connection, Pool], uuid: str, username: str, info: str):
    """
    :param conn:
    :param uuid:
    :param username:
    :param info:
    :return:
    """
    await conn.execute("""
        INSERT INTO userinfo (uuid, username, info)
        VALUES ($1, $2, $3)
        """, uuid, username, info)


async def get_table_userinfo(conn: Connection):
    return await conn.fetch("""
        SELECT address, chainid, hash_email, email_token::TEXT, github_token, time::TEXT
        FROM userinfo;
        """)
