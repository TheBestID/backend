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
            registered          BOOL        DEFAULT FALSE
        );
        ''')
    return True


async def add_user(conn: Union[Connection, Pool], address: str, chainid: str, uuid: str):
    """
    :param conn:            Объект подключения к БД
    :param chainid:
    :param uuid:             Идентификатор sbt
    :param address:         Адрес кошелька
    :return:                Идентификатор пользователя
    """
    await conn.execute("""
        INSERT INTO users (address, chainid, uuid)
        VALUES ($1, $2, $3)
        """, address, chainid, uuid)


async def reg_user(conn: Union[Connection, Pool], address: str, chainid: UUID):
    """
    :param conn:            Объект подключения к БД
    :param chainid:
    :param address:         Адрес кошелька
    :return:                Идентификатор пользователя
    """
    await conn.execute("""
        UPDATE users 
        SET registered = True
        WHERE address = $1 AND chainid = $2;
        """, address, chainid)


async def check(conn: Union[Connection, Pool], address: str, chainId: str) -> bool:
    """
    Проверяет наличие пользователя по кошельку

    :param conn:        Объект подключения к БД
    :param address:     Адрес кошелька
    :param chainId:     ID сети
    :return:            True - найден, иначе False
    """
    res = await conn.fetchrow("""
        SELECT registered
        FROM users
        WHERE address = $1 AND chainid = $2;
        """, address, chainId)
    if res:
        return res['registered']
    return False


async def get_database(conn: Union[Connection, Pool]) -> list:
    """
    Возвращает бд

    :param conn:        Объект подключения к БД
    :return:
    """
    return await conn.fetch("""
        SELECT address, chainid, registered
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
    await conn.execute("""
        DELETE FROM usersinfo;
        """)
    return


async def get_uuid(conn: Union[Connection, Pool], address: str, chainId: str):
    """
    Возвращает uuid по адресу с конкретным chain_id

    :param chainId:
    :param address:
    :param conn:        Объект подключения к БД
    :return:
    """

    return (await conn.fetchrow("""
        SELECT uuid
        FROM users
        WHERE address = $1 AND chainid = $2;
        """, address, chainId))['uuid']

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
