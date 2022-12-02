from typing import Union
from uuid import UUID

from asyncpg import Connection, Pool


async def create_table_achievements(conn: Union[Connection, Pool], clear=False) -> bool:
    """
    :param conn:
    :param clear:
    :return:
    """
    if clear:
        await conn.execute('DROP TABLE IF EXISTS achievements')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS achievements(
            sbt_id              UUID        PRIMARY KEY,
            from_adr            UUID        NOT NULL,
            to_adr              UUID        NOT NULL,
            cid                 TEXT        NOT NULL,
            image_cid           TEXT        NOT NULL,
            type                INT         NOT NULL,
            time                TIMESTAMP   DEFAULT NOW(),
            tx_hash             TEXT        NOT NULL
        );
        ''')
    return True


async def get_table_achievements(conn: Connection):
    return await conn.fetch("""
        SELECT sbt_id::TEXT, from_adr::TEXT, to_adr::TEXT, cid, image_cid, type, time::TEXT, tx_hash
        FROM achievements;
        """)


async def get_owned_ach_by_uuid(conn: Connection, uuid: UUID):
    return await conn.fetch("""
        SELECT image_cid, cid, type
        FROM achievements
        WHERE to_adr = $1;
        """, uuid)


async def get_created_ach_by_uuid(conn: Connection, uuid: UUID):
    return await conn.fetch("""
        SELECT cid, type
        FROM achievements
        WHERE from_adr = $1;
        """, uuid)
