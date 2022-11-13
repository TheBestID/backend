from typing import Union
from uuid import UUID

from asyncpg import Connection, Pool


async def create_table_users(conn: Union[Connection, Pool], clear=False) -> bool:
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
            chainid             INT         NOT NULL,
            uuid                UUID        NOT NULL,
            registered          BOOL        DEFAULT False,
            cid_cv              TEXT        DEFAULT ''
        );
        ''')
    return True


async def get_table_users(conn: Union[Connection, Pool]) -> list:
    """
    :param conn:
    :return:
    """
    return await conn.fetch("""
        SELECT address, chainid, registered, uuid::TEXT
        FROM users;
        """)


async def add_user(conn: Union[Connection, Pool], address: str, chainId: str, uuid: UUID):
    """
    :param conn:
    :param chainId:
    :param uuid:
    :param address:
    :return:
    """
    await conn.execute("""
        INSERT INTO users (address, chainid, uuid)
        VALUES ($1, $2, $3)
        """, str(address).lower(), int(chainId), uuid)


async def reg_user(conn: Union[Connection, Pool], address: str, chainId: UUID):
    """
    :param conn:
    :param chainId:
    :param address:
    :return:
    """
    await conn.execute("""
        UPDATE users 
        SET registered = True
        WHERE address = $1 AND chainid = $2;
        """, str(address).lower(), int(chainId))


async def checkReg(conn: Union[Connection, Pool], address: str, chainId: str) -> bool:
    """
    :param conn:
    :param address:
    :param chainId:
    :return:
    """
    res = await conn.fetchrow("""
        SELECT registered
        FROM users
        WHERE address = $1 AND chainid = $2;
        """, str(address).lower(), int(chainId))
    if res:
        return res['registered']
    return False


async def check(conn: Union[Connection, Pool], address: str, chainId: str) -> bool:
    """
    :param conn:
    :param address:
    :param chainId:
    :return:
    """
    return bool(await conn.fetchrow("""
        SELECT uuid
        FROM users
        WHERE address = $1 AND chainid = $2;
        """, str(address).lower(), int(chainId)))


async def clear_users(conn: Union[Connection, Pool]):
    """
    :param conn:
    :return:
    """
    await conn.execute("""
        DELETE FROM users;
        """)
    return


async def get_uuid(conn: Union[Connection, Pool], address: str, chainId: str) -> Union[UUID, None]:
    """
    :param chainId:
    :param address:
    :param conn:
    :return:
    """
    res = await conn.fetchrow("""
        SELECT uuid
        FROM users
        WHERE address = $1 AND chainid = $2;
        """, str(address).lower(), int(chainId))
    if res:
        return res.get('uuid')
    return None

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
