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
        await conn.execute('DROP TABLE IF EXISTS verify')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS verify(
            address             TEXT        PRIMARY KEY,
            hash_email          TEXT        NOT NULL,
            email_token         UUID        NOT NULL,
            github_token        TEXT        NOT NULL
        );
        ''')
    return True


async def add_verify(conn: Connection, address: str, hash_email: bytes, email_token: UUID, github_token: bytes):
    await conn.execute("""
        INSERT INTO verify (address, hash_email, email_token, github_token)
        VALUES ($1, $2, $3, $4)
        """, address, hash_email, email_token, github_token)


async def check_verify(conn: Connection, address: str, hash_email: bytes, email_token: UUID, github_token: bytes):
    await conn.execute("""
        SELECT registered
        FROM users
        WHERE address = $1 AND chainid = $2;
        """, address, hash_email, email_token, github_token)
