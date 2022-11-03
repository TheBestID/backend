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
            uuid                UUID        ,
            info                TEXT        DEFAULT ''
        );
        ''')
    return True


async def get_info(conn: Union[Connection, Pool]) -> list:
    """
    Возвращает бд

    :param conn:        Объект подключения к БД
    :return:
    """
    return await conn.fetch("""
        SELECT id, address, email, sbt
        FROM users;
        """)
