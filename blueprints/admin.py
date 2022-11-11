from sanic import Blueprint
from sanic.response import Request, json, empty

from database.userinfo import create_table_userinfo, get_table_userinfo
from database.users import create_table_users, get_table_users
from database.verify import create_table_verify, get_table_verify

admin = Blueprint("admin", url_prefix="/admin")


@admin.get("/get_bd_users")
async def get_bd_users(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_table_users(conn))))


@admin.get("/clear_bd_users")
async def clear_bd_users(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create_table_users(conn, True)
        return empty()


@admin.get("/get_bd_userinfo")
async def get_bd_userinfo(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_table_userinfo(conn))))


@admin.get("/clear_bd_userinfo")
async def clear_bd_userinfo(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create_table_userinfo(conn, True)
        return empty()


@admin.get("/get_bd_verify")
async def get_bd_verify(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_table_verify(conn))))


@admin.get("/clear_bd_verify")
async def clear_bd_verify(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create_table_verify(conn, True)
        return empty()
