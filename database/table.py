from typing import Union

from asyncpg import Connection, Pool


async def create(conn: Union[Connection, Pool], clear=False) -> bool:
    """
    Создает таблицу users

    :param conn: Объект подключения к БД
    :param clear:  If True -> очистить таблицу
    :return: str
    """
    if clear:
        await conn.execute('DROP TABLE IF EXISTS users')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id                  SERIAL                  PRIMARY KEY,
            address             TEXT                    NOT NULL            UNIQUE,
            github              TEXT                    DEFAULT NULL        UNIQUE,
            email               VARCHAR(100)            DEFAULT NULL        UNIQUE,
            sbt                 TEXT                    DEFAULT NULL        UNIQUE,
            registered_at       TIMESTAMP               DEFAULT NOW()   
        );
        ''')
    return True


async def insert_address(conn: Union[Connection, Pool], address: str):
    """
    :param conn:            Объект подключения к БД
    :param address:         Адрес кошелька
    :return:                Идентификатор пользователя
    """
    return (await conn.fetchrow("""
        INSERT INTO users (address)
        VALUES ($1)
        RETURNING id;
        """, address))['id']


async def insert_github(conn: Union[Connection, Pool], github: str, uid: int):
    """
    :param conn:            Объект подключения к БД
    :param github:          Что-то с github
    :param uid:             Идентификатор пользователя
    :return:
    """
    await conn.execute("""
        UPDATE users 
        SET github = $1
        WHERE id = $2;
        """, github, uid)
    return True


async def insert_email(conn: Union[Connection, Pool], email: str, address: int):
    """
    :param conn:            Объект подключения к БД
    :param email:           Почта пользователя
    :param address:         Адрес кошелька
    :return:
    """
    await conn.execute("""
        UPDATE users 
        SET email = $1
        WHERE address = $2;
        """, email, address)
    return True


async def check_address(conn: Union[Connection, Pool], address: str) -> bool:
    """
    Проверяет наличие пользователя по кошельку

    :param conn:        Объект подключения к БД
    :param address:     Адрес кошелька
    :return:            True - найден, иначе False
    """
    return bool(await conn.fetchrow("""
        SELECT address
        FROM users
        WHERE address = $1;
        """, address))


async def check_github(conn: Union[Connection, Pool], address: str) -> dict:
    """
    Проверяет наличие пользователя по github

    :param conn:        Объект подключения к БД
    :param address:     Адрес кошелька
    :return:            address, github - найден, иначе None
    """
    return await conn.fetchrow("""
        SELECT address, github
        FROM users
        WHERE address = $1;
        """, address)


async def get_database(conn: Union[Connection, Pool]) -> list:
    """
    Возвращает бд

    :param conn:        Объект подключения к БД
    :return:
    """
    return await conn.fetch("""
        SELECT id, address, email, sbt
        FROM users;
        """)
