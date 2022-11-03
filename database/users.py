from typing import Union
from uuid import UUID

from asyncpg import Connection, Pool


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
            address             TEXT        PRIMARY KEY,
            chainid             TEXT        NOT NULL,
            uuid                UUID        NOT NULL,
            registered          BOOL        DEFAULT FALSE,
            info                TEXT        DEFAULT ''
        );
        ''')
    return True


async def add_user(conn: Union[Connection, Pool], address: str, uid: UUID, txHash: str):
    """
    :param conn:            Объект подключения к БД
    :param txHash:
    :param uid:             Идентификатор sbt
    :param address:         Адрес кошелька
    :return:                Идентификатор пользователя
    """
    await conn.execute("""
        INSERT INTO users (address, uid, txhash)
        VALUES ($1, $2, $3)
        """, address, uid, txHash)


async def check(conn: Union[Connection, Pool], address: str, chainId: str) -> bool:
    """
    Проверяет наличие пользователя по кошельку

    :param conn:        Объект подключения к БД
    :param address:     Адрес кошелька
    :param chainId:     ID сети
    :return:            True - найден, иначе False
    """
    return (await conn.fetchrow("""
        SELECT registered
        FROM users
        WHERE address = $1 AND checkid = $2;
        """, address, chainId))['registered']


async def get_database(conn: Union[Connection, Pool]) -> list:
    """
    Возвращает бд

    :param conn:        Объект подключения к БД
    :return:
    """
    return await conn.fetch("""
        SELECT id, address, email, sbt
        FROM users;
        """)


async def clear_database(conn: Union[Connection, Pool]):
    """

    :param conn:        Объект подключения к БД
    :return:
    """
    await conn.execute("""
        DELETE FROM users;
        """)
    return

# async def main():
#     conn = await connect(host=host, user=username, password=password, database=database)
#     for i in range(50):
#         start = time.time()
#         a = list(map(dict, await get_database(conn)))
#         print(time.time() - start)
#     await conn.close()
#
#
# asyncio.run(main())
