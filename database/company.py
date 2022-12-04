from typing import Union
from uuid import UUID

from asyncpg import Connection, Pool


async def create_table_companies(conn: Union[Connection, Pool], clear=False) -> bool:
    """
    :param conn:
    :param clear:
    :return:
    """
    if clear:
        await conn.execute('DROP TABLE IF EXISTS companies')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS companies(
            address             TEXT        PRIMARY KEY,
            chainid             INT         NOT NULL,
            blockchain          TEXT        NOT NULL,
            uuid                UUID        NOT NULL,
            registered          BOOL        DEFAULT False,
            email               TEXT        DEFAULT '',
            link                TEXT        DEFAULT ''
        );
        ''')
    return True


async def get_table_companies(conn: Union[Connection, Pool]) -> list:
    """
    :param conn:
    :return:
    """
    return await conn.fetch("""
        SELECT address, chainid, blockchain, registered, uuid::TEXT, link
        FROM companies;
        """)


async def add_company(conn: Union[Connection, Pool], address: str, chainId: str, uuid: UUID, blockchain: str, link: str):
    """
    :param conn:
    :param chainId:
    :param uuid:
    :param address:
    :param blockchain:
    :return:
    """
    await conn.execute("""
        INSERT INTO companies (address, chainid, uuid, blockchain, link)
        VALUES ($1, $2, $3, $4, $5)
        """, str(address).lower(), int(chainId), uuid, blockchain.lower(), link.lower())


async def reg_company(conn: Union[Connection, Pool], address: str, chainId: UUID, blockchain: str):
    """
    :param conn:
    :param chainId:
    :param address:
    :param blockchain:
    :return:
    """
    await conn.execute("""
        UPDATE companies
        SET registered = True
        WHERE address = $1 AND chainid = $2 AND blockchain = $3;
        """, str(address).lower(), int(chainId), blockchain.lower())


async def checkRegComp(conn: Union[Connection, Pool], address: str, chainId: str, blockchain: str) -> bool:
    """
    :param conn:
    :param address:
    :param chainId:
    :param blockchain:
    :return:
    """
    res = await conn.fetchrow("""
        SELECT uuid
        FROM companies
        WHERE address = $1 AND chainid = $2 AND blockchain = $3 AND registered = True;
        """, str(address).lower(), int(chainId), blockchain.lower())
    if res:
        return True
    return False


async def checkReg_by_uid_Comp(conn: Union[Connection, Pool], uid: str) -> bool:
    """
    :param conn:
    :param uid:
    :return:
    """
    res = await conn.fetchrow("""
        SELECT registered
        FROM companies
        WHERE uuid = $1;
        """, uid)
    if res:
        return res.get('registered')
    return False


async def check_company(conn: Union[Connection, Pool], address: str, chainId: str, blockchain: str) -> bool:
    """
    :param conn:
    :param address:
    :param chainId:
    :param blockchain:
    :return:
    """
    return bool(await conn.fetchrow("""
        SELECT uuid
        FROM companies
        WHERE address = $1 AND chainid = $2 AND blockchain = $3;
        """, str(address).lower(), int(chainId), blockchain.lower()))


async def get_uuid_comp(conn: Union[Connection, Pool], address: str, chainId: str, blockchain: str) -> Union[UUID, None]:
    """
    :param chainId:
    :param address:
    :param conn:
    :param blockchain:
    :return:
    """
    res = await conn.fetchrow("""
        SELECT uuid
        FROM companies
        WHERE address = $1 AND chainid = $2 AND blockchain = $3;
        """, str(address).lower(), int(chainId), blockchain.lower())
    if res:
        return res.get('uuid')
    return None
