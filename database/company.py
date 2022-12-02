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
            cid_cv              TEXT        DEFAULT '',
            link                TEXT        DEFAULT ''
        );
        ''')
    return True

async def create_table_temple_req(conn: Union[Connection, Pool], clear=False) -> bool:
    """
    :param conn:
    :param clear:
    :return:
    """
    if clear:
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


async def add_req(conn: Union[Connection, Pool], address: str, chainId: str, blockchain: str, link: str, email: str):
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
        VALUES ($1, $2, $3, $4)
        """, str(address).lower(), int(chainId), blockchain.lower(), link.lower(), email.lower())


async def transfer_to_company(conn: Union[Connection, Pool], address: str, chainId: str, blockchain: str, uuid: UUID, tx_hash: str) -> bool:
    data = await conn.fetchrow("""
        SELECT *
        FROM comp_request
        WHERE address = $1 AND chainid = $2 AND blockchain = $3;
        """, address, chainId, blockchain)

    if data:
        await conn.execute("""
            INSERT INTO companies (address, chainid, blockchain, email, link, uuid, tx_hash)
            VALUES ($1, $2, $3, $4, $5, $6);
            """, data['address'], data['chainid'], data['blockchain'], data['email'], data['link'], uuid, tx_hash)
        await conn.execute("""
            DELETE FROM comp_request
            WHERE address = $1 AND chainid = $2 and blockchain = $3;
            """, address, chainId, blockchain)

        return True

    return False



async def get_table_companies(conn: Union[Connection, Pool]) -> list:
    """
    :param conn:
    :return:
    """
    return await conn.fetch("""
        SELECT address, chainid, blockchain, registered, uuid::TEXT, blockchain, link
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
        FROM companies
        WHERE address = $1 AND chainid = $2 AND blockchain = $3;
        """, str(address).lower(), int(chainId), blockchain.lower())
    if res:
        return res.get('registered')
    return False


async def checkReg_by_uid(conn: Union[Connection, Pool], uid: str) -> bool:
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
        FROM companies
        WHERE address = $1 AND chainid = $2 AND blockchain = $3;
        """, str(address).lower(), int(chainId), blockchain.lower())
    if res:
        return res.get('uuid')
    return None


async def check_link(link: str, email: str):
    if domain.find("@") > 0 and domain.find(".") > 0:
        domain = email[email.find("@") + 1 : email.find(".")]
    else:
        return False

    return (domain.lower() in link.lower())