from typing import Union
from uuid import UUID

from asyncpg import Connection, Pool
from sanic.response import json

from utils import create_dump, loadToIpfs, getFromIpfs

prefix = 'https://ipfs.io/ipfs/'


async def create_table_vacancy(conn: Union[Connection, Pool], clear=False) -> bool:
    if clear:
        await conn.execute('DROP TABLE IF EXISTS vacancy')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS vacancy(
            sbt_id              UUID        PRIMARY KEY,
            owner_uuid          UUID        NOT NULL,
            cid                 TEXT        NOT NULL,
            price               INT         NOT NULL,
            category            TEXT        DEFAULT '',
            time                TIMESTAMP   DEFAULT NOW(),
            tx_hash             TEXT        NOT NULL
        );
        ''')
    return True


async def get_table_vacancy(conn: Connection):
    return await conn.fetch("""
        SELECT sbt_id::TEXT, owner_uuid::TEXT, cid, price, category, time::TEXT, tx_hash
        FROM vacancy;
        """)


async def get_owned_vac_by_uuid(conn: Connection, uuid: UUID):
    return await conn.fetch("""
        SELECT cid, type
        FROM vacancy
        WHERE owner_uuid = $1;
        """, uuid)


async def get_vacancies_page(conn: Union[Connection, Pool]) -> list:
    return await conn.fetch("""
        SELECT sbt_id::TEXT, owner_uuid::TEXT, price, category, time::TEXT
        FROM vacancy
        ORDER BY time DESC
        LIMIT 5;
        """)


async def isCreated(conn: Union[Connection, Pool], sbt_id: int) -> bool:
    return bool(await conn.fetchrow("""
        SELECT sbt_id
        FROM vacancy
        WHERE sbt_id = $1;
        """, sbt_id))


############################################

async def get_vacancy(conn: Union[Connection, Pool], sbt_id: int):
    cid = (await conn.fetchrow("""
        SELECT cid
        FROM vacancy WHERE sbt_id = $1;
        """, sbt_id)).get('cid')
    data = getFromIpfs(cid)
    return json(
        {'owner_uuid': data.get('attributes')[1].get('owner_uuid'), 'price': data.get('attributes')[3].get('price'),
         'category': data.get('attributes')[2].get('category'), 'info': data.get('description'), 'id': id})


async def get_previews_sort_by_int(conn: Union[Connection, Pool], sort_value: str, offset_number: int, top_number: int,
                                   in_asc: bool) -> list:
    if in_asc:
        return await conn.fetch("""
            SELECT sbt_id::TEXT, owner_uuid::TEXT price, category, time::TEXT
            FROM vacancy 
            ORDER BY $1 ASC 
            LIMIT $2 
            OFFSET $3 ROW;
            """, sort_value, top_number, offset_number)
    else:
        return await conn.fetch("""
            SELECT sbt_id::TEXT, owner_uuid::TEXT price, category, time::TEXT
            FROM vacancy 
            ORDER BY $1 DESC 
            LIMIT $2 
            OFFSET $3 ROW;
            """, sort_value, top_number, offset_number)


async def isAllowed(conn: Union[Connection, Pool], sender_uuid: UUID, id: int):
    if str(sender_uuid) == (await conn.fetchrow("""
        SELECT owner_uuid
        FROM vacancy
        WHERE id = $1;
        """, id)).get('owner_uuid'):
        return True

    else:
        return False


async def addSBTvac():
    # some work to
    pass


# what is the defualt type of timestamp?


async def getUuidByid(conn: Union[Connection, Pool], id: int):
    return (await conn.fetchrow("""
        SELECT ach_uuid
        FROM vacancy
        WHERE id = $1;
        """, id)).get('ach_uuid')


async def add_vacancy(conn: Union[Connection, Pool], owner_uuid: UUID, price: int, category: str, info: str,
                      ach_uuid: str, key) -> str:
    data = create_dump('username', info, False,
                       attributes=[{'type achivement': 'vacancy'}, {'owner_uuid': str(owner_uuid)},
                                   {'category': category}, {'price': price}, {'ach_uuid': ach_uuid}])
    cid = await loadToIpfs(data, key)

    await conn.execute("""
        INSERT INTO vacancy (owner_uuid, ach_uuid, price, category, info, ipfs_cid)
        VALUES ($1, $2, $3, $4, $5, $6);
        """, owner_uuid, ach_uuid, price, category, info, cid)

    return cid


# doesn't work correctly


async def get_previews_sort_by_str(conn: Union[Connection, Pool], sort_type: str, sort_value: str, sort_value_int: str,
                                   offset_number: int, top_number: int, in_asc: bool) -> list:
    return await conn.fetch("""
             SELECT id, owner_uuid, price, category, timestamp::TEXT
             FROM vacancy 
             WHERE $1 = $2 
             ORDER BY $3 
             LIMIT $4 
             OFFSET $5 ROW;
             """, sort_type, sort_value, sort_value_int, top_number, offset_number)
    # in_asc = True
    # if in_asc:
    #     return await conn.fetch("""
    #         SELECT owner_uuid, price, category, timestamp::TEXT
    #         FROM vacancy WHERE $1 = $2 ORDER BY $3 LIMIT $4 OFFSET $5 ROW;
    #         """, sort_type, sort_value, sort_value_int, top_number, offset_number)

    # else:
    #     return await conn.fetch("""
    #         SELECT owner_uuid, price, category, timestamp::TEXT
    #         FROM vacancy WHERE $1 = $2 ORDER BY $3 DESC LIMIT $4 OFFSET $5 ROW;
    #         """, sort_type, sort_value, sort_value_int, top_number, offset_number)


# change create_dump: add ach_uuid!!!
async def edit_vacancy(conn: Union[Connection, Pool], id: int, price: int, category: str, info: str, owner_uuid: str):
    old_cid = (await conn.fetchrow("""
        SELECT ipfs_cid
        FROM vacancy
        WHERE id = $1;
        """, id)).get('ipfs_cid')

    data = create_dump('username', info, False,
                       attributes=[{'type achivement': 'vacancy'}, {'owner_uuid': str(owner_uuid)},
                                   {'category': category}, {'price': price}, {'last_cid': old_cid}])
    cid = await loadToIpfs(data)
    await conn.fetch("""
        UPDATE vacancy SET price = $1, category = $2, info = $3, ipfs_cid = $5 WHERE id = $4;
    """, price, category, info, id, cid)


async def delete_vacancy(conn: Union[Connection, Pool], id: int):
    await conn.fetch(""" 
    DELETE FROM vacancy WHERE id = $1;    
     """, id)


async def get_database(conn: Union[Connection, Pool]) -> list:
    return await conn.fetch("""
        SELECT id, owner_uuid, ach_uuid, price, category, timestamp::TEXT , info, ipfs_cid
        FROM vacancy;
        """)


async def clear_database(conn: Union[Connection, Pool]):
    """

    :param conn:
    :return:
    """
    await conn.execute("""
        DELETE FROM vacancy;
        """)
    return
