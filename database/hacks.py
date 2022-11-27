from typing import Union
from uuid import UUID
from asyncpg import Connection, Pool


async def isAllowed_():
    # some work connected to chek can user create / delete vacancy
    return True


async def addSBTvac_():
    # some work to
    pass


async def isCreated_(conn: Union[Connection, Pool], id: int) -> bool:
    if (await conn.fetchrow("""
        SELECT id
        FROM hacks
        WHERE id = $1;
        """, id)):
        return True
    else:
        return False


async def create(conn: Union[Connection, Pool], clear=False) -> bool:
    if clear:
        await conn.execute('DROP TABLE IF EXISTS hacks;')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS hacks(
            id                  SERIAL      PRIMARY KEY,
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
            timestamp           TIMESTAMP   DEFAULT NOW(),
            type                TEXT        DEFAULT 'default'
        );
        ''')


    return True


async def add_hack(conn: Union[Connection, Pool],
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
                   category: str
                   ):
    """
    """
    await conn.execute("""
        INSERT INTO hacks (owner_uuid, theme, base_color, font_head, font_par, hackathon_name, description,back_url,logo_url,price,pool,descr_price,sbt_url,task_descr,social_link, category  )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16);
        """, owner_uuid, theme, base_color, font_head, font_par, hackathon_name, description, back_url, logo_url, price,
                       pool, descr_price, sbt_url, task_descr, social_link, category)


async def get_previews_sort_by_int(conn: Union[Connection, Pool], sort_value: str, offset_number: int, top_number: int,
                                   in_asc: bool) -> list:
    # in_asc = True
    if in_asc:
        return await conn.fetch("""
            SELECT hackathon_name, logo_url, owner_uuid, price, category, timestamp::TEXT
            FROM hacks ORDER BY $1 ASC LIMIT $2 OFFSET $3 ROW;
            """, sort_value, top_number, offset_number)

    else:
        return await conn.fetch("""
            SELECT hackathon_name, logo_url, owner_uuid, price, category, timestamp::TEXT
            FROM hacks ORDER BY $1 DESC LIMIT $2 OFFSET $3 ROW;
            """, sort_value, top_number, offset_number)


# doesn't work correctly
async def get_previews_sort_by_str(conn: Union[Connection, Pool], sort_type: str, sort_value: str, sort_value_int: str,
                                   offset_number: int, top_number: int, in_asc: bool) -> list:
    return await conn.fetch("""
             SELECT hackathon_name, logo_url, owner_uuid, price, category, timestamp::TEXT
             FROM hacks WHERE $1 = $2 ORDER BY $3 LIMIT $4 OFFSET $5 ROW;
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


async def get_hack(conn: Union[Connection, Pool], id: int) -> list:
    return await conn.fetch("""
        SELECT owner_uuid::TEXT, theme, base_color, font_head, font_par, hackathon_name, description,back_url,logo_url,price,pool,descr_price,sbt_url,task_descr,social_link, category, timestamp::TEXT
        FROM hacks WHERE id = $1;
        """, id)


async def edit_hack(conn: Union[Connection, Pool], id: int, price: int, category: str, info: str):
    await conn.fetch("""
        UPDATE hacks SET price = $1, category = $2, info = $3 WHERE id = $4;
    """, price, category, info, id)


async def delete_hack(conn: Union[Connection, Pool], id: int):
    await conn.fetch(""" 
    DELETE FROM hacks WHERE id = $1;    
     """, id)


async def get_database(conn: Union[Connection, Pool]) -> list:
    return await conn.fetch("""
        SELECT id, owner_uuid::TEXT , price, category, timestamp::TEXT , description
        FROM hacks;
        """)


async def clear_database(conn: Union[Connection, Pool]):
    await conn.execute("""
        DELETE FROM hacks;
        """)
    return
