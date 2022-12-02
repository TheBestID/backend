from typing import Union
from uuid import UUID

from asyncpg import Connection, Pool


async def create_table_ach_request(conn: Union[Connection, Pool], clear=False) -> bool:
    """
    :param conn:
    :param clear:
    :return:
    """
    if clear:
        await conn.execute('DROP TABLE IF EXISTS ach_request')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS ach_request(
            sbt_id              UUID        PRIMARY KEY,
            from_adr            UUID        NOT NULL,
            to_adr              UUID        NOT NULL,
            cid                 TEXT        NOT NULL,
            image_cid           TEXT        NOT NULL,
            type                INT         NOT NULL,
            time                TIMESTAMP   DEFAULT NOW()
        );
        ''')
    return True


async def get_table_ach_request(conn: Connection):
    return await conn.fetch("""
        SELECT sbt_id::TEXT, from_adr::TEXT, to_adr::TEXT, cid, image_cid, type, time::TEXT
        FROM ach_request;
        """)


async def add_ach_request(conn: Union[Connection, Pool], sbt_id: UUID, _from: UUID, to: UUID, cid: str, image_cid: str,
                          _type: int):
    """
    :param conn:
    :param sbt_id:
    :param _from:
    :param to:
    :param cid:
    :param image_cid:
    :param _type:
    :return:
    """
    await conn.execute("""
        INSERT INTO ach_request (sbt_id, from_adr, to_adr, cid, image_cid, type)
        VALUES ($1, $2, $3, $4, $5, $6);
        """, sbt_id, _from, to, cid, image_cid, _type)


async def del_ach_request(conn: Union[Connection, Pool], sbt_id: UUID):
    """
    :param conn:
    :param sbt_id:
    :return:
    """
    await conn.execute("""
        DELETE FROM ach_request
        WHERE sbt_id = $1;
        """, sbt_id)


async def transfer_to_achievements(conn: Union[Connection, Pool], sbt_id: UUID, from_adr: UUID, tx_hash: str):
    data = await conn.fetchrow("""
        SELECT *
        FROM ach_request
        WHERE sbt_id = $1 AND from_adr = $2;
        """, sbt_id, from_adr)

    if data:
        await conn.execute("""
            INSERT INTO achievements (sbt_id, from_adr, to_adr, cid, image_cid, type, tx_hash)
            VALUES ($1, $2, $3, $4, $5, $6);
            """, data['sbt_id'], data['from_adr'], data['to_adr'], data['cid'], data['image_cid'], data['type'],
                           tx_hash)
        await conn.execute("""
            DELETE FROM ach_request
            WHERE sbt_id = $1 AND from_adr = $2;
            """, sbt_id, from_adr)

        return True

    return False
