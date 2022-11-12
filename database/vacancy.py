from typing import Union
from uuid import UUID
from sanic.response import json
from asyncpg import Connection, Pool

from database.users import get_uuid
from utils import create_dump, loadToIpfs, getFromIpfs


prefix = 'https://ipfs.io/ipfs/'


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
    #some work to 
    pass


async def getUuidByid(conn: Union[Connection, Pool], id: int):
    return await conn.fetchrow("""
        SELECT ach_uuid
        FROM vacancy
        WHERE id = $1;
        """, id)


async def isCreated(conn: Union[Connection, Pool], id: int) -> bool:

    if (await conn.fetchrow("""
        SELECT id
        FROM vacancy
        WHERE id = $1;
        """, id)):
        return True
    else:
        return False


async def create(conn: Union[Connection, Pool], clear=False) -> bool:
    if clear:
        await conn.execute('DROP TABLE IF EXISTS vacancy')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS vacancy(
            id                  SERIAL      PRIMARY KEY,
            ach_uuid            TEXT        DEFAULT '',
            owner_uuid          TEXT        DEFAULT '',
            price               INT         NOT NULL,
            category            TEXT        DEFAULT '',
            timestamp           TIMESTAMP   DEFAULT NOW(),
            info                TEXT        NOT NULL,
            ipfs_cid            TEXT        NOT NULL
            
        );
        ''')
    return True



# what is the defualt type of timestamp?
async def add_vacancy(conn: Union[Connection, Pool], owner_uuid: UUID, price: int, category: str, info: str, ach_uuid: str):
    data = create_dump('username', info, False, attributes=[{'type achivement': 'vacancy'}, {'owner_uuid': str(owner_uuid)}, {'category': category}, {'price': price}, {'ach_uuid':ach_uuid}])
    cid = await loadToIpfs(data)
    
    await conn.execute("""
        INSERT INTO vacancy (owner_uuid, ach_uuid, price, category, info, ipfs_cid)
        VALUES ($1, $2, $3, $4, $5, $6);
        """, owner_uuid, ach_uuid, price, category, info, cid)
    
    


async def get_previews_sort_by_int(conn: Union[Connection, Pool], sort_value: str, offset_number: int,  top_number: int, in_asc: bool) -> list:
    #in_asc = True
    if in_asc:
        return await conn.fetch("""
            SELECT owner_uuid, price, category, timestamp::TEXT
            FROM vacancy 
            ORDER BY $1 ASC 
            LIMIT $2 
            OFFSET $3 ROW;
            """, sort_value, top_number, offset_number)

    else:
        return await conn.fetch("""
            SELECT owner_uuid, price, category, timestamp::TEXT
            FROM vacancy 
            ORDER BY $1 DESC 
            LIMIT $2 
            OFFSET $3 ROW;
            """, sort_value, top_number, offset_number)


#doesn't work correctly
async def get_previews_sort_by_str(conn: Union[Connection, Pool], sort_type: str, sort_value: str, sort_value_int: str, offset_number: int,  top_number: int, in_asc: bool) -> list:
    return await conn.fetch("""
             SELECT owner_uuid, price, category, timestamp::TEXT
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

async def get_vacancy(conn: Union[Connection, Pool], id: int):
    cid = (await conn.fetchrow("""
        SELECT ipfs_cid
        FROM vacancy WHERE id = $1;
        """, id)).get('ipfs_cid')
    data = getFromIpfs(cid)
    return json({'owner_uuid': data.get('attributes')[1].get('owner_uuid'), 'price': data.get('attributes')[3].get('price'), 'category': data.get('attributes')[2].get('category'), 'info': data.get('description') })


#change create_dump: add ach_uuid!!!
async def edit_vacancy(conn: Union[Connection, Pool], id: int, price: int, category: str, info: str, owner_uuid: str):
    data = create_dump('username', info, False, attributes=[{'type achivement': 'vacancy'}, {'owner_uuid': str(owner_uuid)}, {'category': category}, {'price': price}])
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

    :param conn:        Объект подключения к БД
    :return:
    """
    await conn.execute("""
        DELETE FROM vacancy;
        """)
    return