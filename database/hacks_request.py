from typing import Union
from uuid import UUID

from asyncpg import Connection, Pool
from sanic.response import json



async def create_table_hack_request(conn: Union[Connection, Pool], clear=False) -> bool:
    if clear:
        await conn.execute('DROP TABLE IF EXISTS hacks_request')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS hacks_request(
            id                  UUID        PRIMARY KEY,
            owner_uuid          UUID        NOT NULL,
            theme               TEXT        DEFAULT 'Dark',
            base_color          TEXT        DEFAULT 'White',
            font_head           TEXT        DEFAULT '',
            font_par            TEXT        DEFAULT '',
            hackathon_name      TEXT        DEFAULT '',
            description         TEXT        DEFAULT '',
            back_url            TEXT        DEFAULT 'http:',
            logo_url            TEXT        DEFAULT 'http:',         
            price               INT         NOT NULL,
            pool                TEXT        DEFAULT '0/0/0/0',
            descr_price         TEXT        DEFAULT '',
            sbt_url             TEXT        DEFAULT 'http:',
            task_descr          TEXT        DEFAULT '',
            social_link         TEXT        DEFAULT '',
            category            TEXT        DEFAULT '',
            type                TEXT        DEFAULT 'default',
            start_date          TEXT        NOT NULL,
            end_date            TEXT        NOT NUll
        );
        ''')
    return True


async def get_table_hack_request(conn: Connection):
    return await conn.fetch("""
        SELECT id::TEXT, owner_uuid::TEXT, price, category, start_date, end_date
        FROM hacks_request;
        """)


async def add_hack_request(conn: Union[Connection, Pool],
                   hack_id: UUID,
                   owner_uuid: UUID,
                   theme: str,
                   base_color: str,
                   font_head: str,
                   font_par: str,
                   hackathon_name: str,
                   description: str,
                   back_url: str,
                   logo_url: str,
                   price: int,
                   pool: str,
                   descr_price: str,
                   sbt_url: str,
                   task_descr: str,
                   social_link: str,
                   category: str,
                   start_date: str,
                   end_date: str
                   ):
    """
    """
    await conn.execute("""
        INSERT INTO hacks_request (id, owner_uuid, theme, base_color, font_head, font_par, hackathon_name, description,back_url,logo_url,price,pool,descr_price,sbt_url,task_descr,social_link, category, start_date, end_date)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19);
        """, hack_id, owner_uuid, theme, base_color, font_head, font_par, hackathon_name, description, back_url, logo_url, price,
                       pool, descr_price, sbt_url, task_descr, social_link, category, start_date, end_date)


async def del_hack_request(conn: Union[Connection, Pool], id: int):
    """
    :param conn:
    :param sbt_id:
    :return:
    """
    await conn.execute("""
        DELETE FROM hacks_request
        WHERE id = $1;
        """, id)


async def transfer_to_hacks(conn: Union[Connection, Pool], hack_id: UUID, owner: UUID, tx_hash: str):
    data = await conn.fetchrow("""
        SELECT *
        FROM hacks_request
        WHERE id = $1 AND owner_uuid = $2;
        """, hack_id, owner)

    if data:
        await conn.execute("""
            INSERT INTO hacks (id, owner_uuid, theme, base_color, font_head, font_par, hackathon_name, description,back_url,logo_url,price,pool,descr_price,sbt_url,task_descr,social_link, category, start_date, end_date, tx_hash )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20);
        """,  data['id'], data['owner_uuid'], data['theme'], data['base_color'], data['font_head'], data['font_par'], data['hackathon_name'], \
             data['description'], data['back_url'], data['logo_url'], data['price'], data['pool'], data['descr_price'], data['sbt_url'], data['task_descr'], data['social_link'], data['category'], data['start_date'], data['end_date'],tx_hash)
        await conn.execute("""
            DELETE FROM hacks_request
            WHERE id = $1 AND owner_uuid = $2;
            """, hack_id, owner)

        return True

    return False
