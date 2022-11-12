from typing import Union

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
