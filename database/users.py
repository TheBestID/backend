from typing import Union
from uuid import UUID

from asyncpg import Connection, Pool


async def create_table_users(conn: Union[Connection, Pool], clear=False) -> bool:
    """
    :param conn:
    :param clear:
    :return:
    """
    if clear:
        await conn.execute('DROP TABLE IF EXISTS users')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users(
            address             TEXT        PRIMARY KEY,
            chainid             INT         NOT NULL,
            blockchain          TEXT        NOT NULL,
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
        SELECT address, chainid, blockchain, registered, uuid::TEXT, blockchain
        FROM users;
        """)


async def add_user(conn: Union[Connection, Pool], address: str, chainId: str, uuid: UUID, blockchain: str):
    """
    :param conn:
    :param chainId:
    :param uuid:
    :param address:
    :param blockchain:
    :return:
    """
    await conn.execute("""
        INSERT INTO users (address, chainid, uuid, blockchain)
        VALUES ($1, $2, $3, $4)
        """, str(address).lower(), int(chainId), uuid, blockchain.lower())


async def reg_user(conn: Union[Connection, Pool], address: str, chainId: UUID, blockchain: str):
    """
    :param conn:
    :param chainId:
    :param address:
    :param blockchain:
    :return:
    """
    await conn.execute("""
        UPDATE users 
        SET registered = True
        WHERE address = $1 AND chainid = $2 AND blockchain = $3;
        """, str(address).lower(), int(chainId), blockchain.lower())


async def checkReg(conn: Union[Connection, Pool], address: str, chainId: str, blockchain: str) -> bool:
    """
    :param conn:
    :param address:
    :param chainId:
    :param blockchain:
    :return:
    """
    res = await conn.fetchrow("""
        SELECT registered
        FROM users
        WHERE address = $1 AND chainid = $2 AND blockchain = $3;
        """, str(address).lower(), int(chainId), blockchain.lower())
    if res:
        return res.get('registered')
    return False


async def check(conn: Union[Connection, Pool], address: str, chainId: str, blockchain: str) -> bool:
    """
    :param conn:
    :param address:
    :param chainId:
    :param blockchain:
    :return:
    """
    return bool(await conn.fetchrow("""
        SELECT uuid
        FROM users
        WHERE address = $1 AND chainid = $2 AND blockchain = $3;
        """, str(address).lower(), int(chainId), blockchain.lower()))


async def get_uuid(conn: Union[Connection, Pool], address: str, chainId: str, blockchain: str) -> Union[UUID, None]:
    """
    :param chainId:
    :param address:
    :param conn:
    :param blockchain:
    :return:
    """
    res = await conn.fetchrow("""
        SELECT uuid
        FROM users
        WHERE address = $1 AND chainid = $2 AND blokchain = $3;
        """, str(address).lower(), int(chainId), blockchain.lower())
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
