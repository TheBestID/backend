from typing import Union
from uuid import UUID

from asyncpg import Connection, Pool


# from config import host, username, password, database


async def create_table_verify(conn: Union[Connection, Pool], clear=False) -> bool:
    """
    :param conn:
    :param clear:
    :return:
    """
    if clear:
        await conn.execute('DROP TABLE IF EXISTS verify')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS verify(
            address             TEXT        PRIMARY KEY,
            chainid             INT         NOT NULL,
            blockchain          TEXT        NOT NULL,
            hash_email          TEXT        NOT NULL,
            email_token         UUID        NOT NULL,
            github_token        TEXT        NOT NULL,
            time                TIMESTAMP   DEFAULT NOW()
        );
        ''')
    return True


async def get_table_verify(conn: Connection):
    return await conn.fetch("""
        SELECT address, chainid, blockchain, hash_email, email_token::TEXT, github_token, time::TEXT
        FROM verify;
        """)


async def add_verify(conn: Connection, address: str, chainId: int, blockchain: str, hash_email: str, email_token: str,
                     github_token: str):
    await conn.execute("""
        INSERT INTO verify (address, chainid, blockchain, hash_email, email_token, github_token)
        VALUES ($1, $2, $3, $4, $5, $6);
        """, str(address).lower(), int(chainId), blockchain.lower(), hash_email, email_token, github_token)


async def check_verify(conn: Connection, address: str, chainId: int, blockchain: str, hash_email: str,
                       email_token: UUID, github_token: str):
    data = await conn.fetchrow("""
        SELECT hash_email, email_token::TEXT, github_token, time
        FROM verify
        WHERE address = $1 AND chainid = $2 AND blockchain = $3;
        """, str(address).lower(), int(chainId), blockchain.lower())
    if not data:
        return False
    if hash_email == data['hash_email'] and email_token == data['email_token'] and github_token == data['github_token']:
        return True
    return False


async def check_in_verify(conn: Connection, address: str, chainId: int, blockchain: str):
    return bool(await conn.fetchrow("""
        SELECT hash_email
        FROM verify
        WHERE address = $1 AND chainid = $2 AND blockchain = $3;
        """, str(address).lower(), int(chainId), blockchain.lower()))


async def del_verify(conn: Connection, address: str, chainId: int, blockchain: str):
    await conn.execute("""
        DELETE
        FROM verify
        WHERE address = $1 AND chainid = $2 AND blockchain = $3;
        """, str(address).lower(), int(chainId), blockchain.lower())
