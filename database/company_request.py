
from typing import Union
from uuid import UUID

from asyncpg import Connection, Pool


async def create_table_temple_req(conn: Union[Connection, Pool], clear=False) -> bool:
    """
    :param conn:
    :param clear:
    :return:
    """
    await conn.execute('DROP TABLE IF EXISTS comp_request')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS comp_request(
            address             TEXT        PRIMARY KEY,
            chainid             INT         NOT NULL,
            blockchain          TEXT        NOT NULL,
            link                TEXT        NOT NULL,
            email               TEXT        NOT NULL
        );
        ''')
    return True


async def get_comp_req(conn: Union[Connection, Pool]):
    """
    :param conn:
    :return:
    """
    return await conn.fetch("""
        SELECT address, chainid, blockchain, link
        FROM comp_request;
        """)





async def add_comp_req(conn: Union[Connection, Pool], address: str, chainId: str, blockchain: str, link: str, email: str):
    """
    :param conn:
    :param chainId:
    :param uuid:
    :param address:
    :param blockchain:
    :return:
    """
    await conn.execute("""
        INSERT INTO comp_request (address, chainid, blockchain, link, email)
        VALUES ($1, $2, $3, $4, $5)
        """, str(address).lower(), int(chainId), blockchain.lower(), link.lower(), email.lower())


async def del_comp_req(conn: Union[Connection, Pool], address: str, chainId: str, blockchain: str):
    await conn.execute("""
        DELETE FROM comp_request
        WHERE address = $1 AND chainid = $2 AND blockchain = $3;
        """, str(address).lower(), int(chainId), blockchain.lower())


async def transfer_to_company(conn: Union[Connection, Pool], address: str, chainId: str, blockchain: str, uuid: UUID) -> bool:
    data = await conn.fetchrow("""
        SELECT *
        FROM comp_request
        WHERE address = $1 AND chainid = $2 AND blockchain = $3;
        """, str(address).lower(), int(chainId), blockchain.lower())

    if data:
        await conn.execute("""
            INSERT INTO companies (address, chainid, blockchain, email, link, uuid)
            VALUES ($1, $2, $3, $4, $5, $6);
            """, data['address'], data['chainid'], data['blockchain'], data['email'], data['link'], uuid)
        await conn.execute("""
            DELETE FROM comp_request
            WHERE address = $1 AND chainid = $2 and blockchain = $3;
            """, str(address).lower(), int(chainId), blockchain.lower())

        return True

    return False



async def check_company_req(conn: Union[Connection, Pool], address: str, chainId: str, blockchain: str) -> bool:
    """
    :param conn:
    :param address:
    :param chainId:
    :param blockchain:
    :return:
    """
    return bool(await conn.fetchrow("""
        SELECT address
        FROM comp_request
        WHERE address = $1 AND chainid = $2 AND blockchain = $3;
        """, str(address).lower(), int(chainId), blockchain.lower()))