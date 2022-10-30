import asyncio
import time
from typing import Union

from asyncpg import Connection, Pool, connect


# from config import host, username, password, database


async def create(conn: Union[Connection, Pool], clear=False) -> bool:
    """
    Создает таблицу users

    :param conn: Объект подключения к БД
    :param clear:  If True -> очистить таблицу
    :return: str
    """
    if clear:
        await conn.execute('DROP TABLE IF EXISTS users')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users(
            uid                 SERIAL                  PRIMARY KEY,
            address             TEXT                    NOT NULL            UNIQUE,
            txhash              TEXT                    NOT NULL            UNIQUE
        );
        ''')
    return True


async def insert_address(conn: Union[Connection, Pool], address: str, txHash: str):
    """
    :param txHash:
    :param conn:            Объект подключения к БД
    :param address:         Адрес кошелька
    :return:                Идентификатор пользователя
    """
    return (await conn.fetchrow("""
        INSERT INTO users (address, txhash)
        VALUES ($1, $2)
        RETURNING uid;
        """, address, txHash))['uid']


async def insert_github(conn: Union[Connection, Pool], github: str, uid: int):
    """
    :param conn:            Объект подключения к БД
    :param github:          Что-то с github
    :param uid:             Идентификатор пользователя
    :return:
    """
    await conn.execute("""
        UPDATE users 
        SET github = $1
        WHERE id = $2;
        """, github, uid)
    return True


async def insert_email(conn: Union[Connection, Pool], email: str, address: int):
    """
    :param conn:            Объект подключения к БД
    :param email:           Почта пользователя
    :param address:         Адрес кошелька
    :return:
    """
    await conn.execute("""
        UPDATE users 
        SET email = $1
        WHERE address = $2;
        """, email, address)
    return True


async def check_address(conn: Union[Connection, Pool], address: str) -> bool:
    """
    Проверяет наличие пользователя по кошельку

    :param conn:        Объект подключения к БД
    :param address:     Адрес кошелька
    :return:            True - найден, иначе False
    """
    return bool(await conn.fetchrow("""
        SELECT address
        FROM users
        WHERE address = $1;
        """, address))


async def check_github(conn: Union[Connection, Pool], address: str) -> dict:
    """
    Проверяет наличие пользователя по github

    :param conn:        Объект подключения к БД
    :param address:     Адрес кошелька
    :return:            address, github - найден, иначе None
    """
    return await conn.fetchrow("""
        SELECT address, github
        FROM users
        WHERE address = $1;
        """, address)


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
