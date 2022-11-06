from typing import Union
from uuid import UUID
import time

from asyncpg import Connection, Pool


async def isAllowed(owner_uuid: UUID):
    #some work connected to chek can user create / delete vacancy
    return True

async def addSBTvac():
    #some work to 
    pass

async def isCreated(conn: Union[Connection, Pool], id: int) -> bool:
    """
    Проверяет наличие вакансии
    """
    
    if (await conn.fetchrow("""
        SELECT id
        FROM vacancy
        WHERE id = $1;
        """, id)):
        return True
    else:
        return False


async def create(conn: Union[Connection, Pool], clear=False) -> bool:
    """
    Создает таблицу vacancy

    :param conn:    Объект подключения к БД
    :param clear:   If True -> очистить таблицу
    :return:
    """
    if clear:
        await conn.execute('DROP TABLE IF EXISTS vacancy')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS vacancy(
            id                  SERIAL      PRIMARY KEY,
            owner_uuid          TEXT        DEFAULT '',
            price               INT         NOT NULL,
            category            TEXT        DEFAULT '',
            timestamp           TIMESTAMP   DEFAULT NOW(),
            info                TEXT        NOT NULL
            
        );
        ''')
    return True



# what is the defualt type of timestamp?
async def add_vacancy(conn: Union[Connection, Pool], owner_uuid: UUID, price: int, category: str, info: str):
    """
    """
    await conn.execute("""
        INSERT INTO vacancy (owner_uuid, price, category, info)
        VALUES ($1, $2, $3, $4);
        """, owner_uuid, price, category, info)


async def get_previews_sort_by_int(conn: Union[Connection, Pool], sort_value: str, offset_number: int,  top_number: int, in_asc: bool) -> list:
    #in_asc = True
    if in_asc:
        return await conn.fetch("""
            SELECT owner_uuid, price, category, timestamp::TEXT
            FROM vacancy ORDER BY $1 ASC LIMIT $2 OFFSET $3 ROW;
            """, sort_value, top_number, offset_number)

    else:
        return await conn.fetch("""
            SELECT owner_uuid, price, category, timestamp::TEXT
            FROM vacancy ORDER BY $1 DESC LIMIT $2 OFFSET $3 ROW;
            """, sort_value, top_number, offset_number)


#doesn't work correctly
async def get_previews_sort_by_str(conn: Union[Connection, Pool], sort_type: str, sort_value: str, sort_value_int: str, offset_number: int,  top_number: int, in_asc: bool) -> list:
    return await conn.fetch("""
             SELECT owner_uuid, price, category, timestamp::TEXT
             FROM vacancy WHERE $1 = $2 ORDER BY $3 LIMIT $4 OFFSET $5 ROW;
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

async def get_vacancy(conn: Union[Connection, Pool], id: int) -> list:
    return await conn.fetch("""
        SELECT owner_uuid, price, category, timestamp::TEXT, info
        FROM vacancy WHERE id = $1;
        """, id)


async def edit_vacancy(conn: Union[Connection, Pool], id: int, price: int, category: str, info: str):
    await conn.fetch("""
        UPDATE vacancy SET price = $1, category = $2, info = $3 WHERE id = $4;
    """, price, category, info, id)


async def delete_vacancy(conn: Union[Connection, Pool], id: int):
    await conn.fetch(""" 
    DELETE FROM vacancy WHERE id = $1;    
     """, id)

async def get_database(conn: Union[Connection, Pool]) -> list:
    """
    Возвращает бд

    :param conn:        Объект подключения к БД
    :return:
    """
    return await conn.fetch("""
        SELECT id, owner_uuid, price, category, timestamp::TEXT , info
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