from typing import Union
from uuid import UUID

from asyncpg import Connection, Pool
from sanic.response import json

from utils import create_dump, loadToIpfs, getFromIpfs


async def create_table_vac_request(conn: Union[Connection, Pool], clear=False) -> bool:
    if clear:
        await conn.execute('DROP TABLE IF EXISTS vac_request')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS vac_request(
            sbt_id              UUID        PRIMARY KEY,
            owner_uuid          UUID        NOT NULL,
            cid                 TEXT        NOT NULL,
            price               INT         NOT NULL,
            category            TEXT        DEFAULT '',
            time                TIMESTAMP   DEFAULT NOW()
        );
        ''')
    return True


async def get_table_vac_request(conn: Connection):
    return await conn.fetch("""
        SELECT sbt_id::TEXT, owner_uuid::TEXT, cid, price, category, time::TEXT, tx_hash
        FROM vac_request;
        """)


async def add_vac_request(conn: Union[Connection, Pool], sbt_id: UUID, owner: UUID, cid: str, price: int,
                          category: str):
    """
    :param conn:
    :param sbt_id:
    :param owner:
    :param price:
    :param cid:
    :param category:
    :return:
    """
    await conn.execute("""
        INSERT INTO vac_request (sbt_id, owner_uuid, cid, price, category)
        VALUES ($1, $2, $3, $4, $5);
        """, sbt_id, owner, cid, price, category)


async def del_vac_request(conn: Union[Connection, Pool], sbt_id: UUID):
    """
    :param conn:
    :param sbt_id:
    :return:
    """
    await conn.execute("""
        DELETE FROM vac_request
        WHERE sbt_id = $1;
        """, sbt_id)


async def transfer_to_vacancy(conn: Union[Connection, Pool], sbt_id: UUID, owner: UUID, tx_hash: str):
    data = await conn.fetchrow("""
        SELECT *
        FROM vac_request
        WHERE sbt_id = $1 AND owner_uuid = $2;
        """, sbt_id, owner)

    if data:
        await conn.execute("""
            INSERT INTO achievements (sbt_id, owner_uuid, cid, price, category, tx_hash)
            VALUES ($1, $2, $3, $4, $5, $6);
            """, data['sbt_id'], data['owner_uuid'], data['cid'], data['price'], data['category'], tx_hash)
        await conn.execute("""
            DELETE FROM vac_request
            WHERE sbt_id = $1 AND owner_uuid = $2;
            """, sbt_id, owner)

        return True

    return False
