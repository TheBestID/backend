from sanic import Blueprint
from sanic.response import Request, json, empty
from uuid import uuid4

from database.achievements import create_table_achievements, get_table_achievements
from database.userinfo import create_table_userinfo, get_table_userinfo, add_user_to_table
from database.users import create_table_users, get_table_users
from database.verify import create_table_verify, get_table_verify
from openapi.user import UserCheck
from sanic_ext import openapi

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


@admin.get("/get_bd_achievements")
async def get_bd_achievements(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_table_achievements(conn))))


@admin.get("/clear_bd_achievements")
async def clear_bd_achievements(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create_table_achievements(conn, True)
        return empty()


@admin.post("/add_user_test")
@openapi.body({"application/json": UserCheck}, required=True)
async def add_user(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        user_uuid = uuid4()
        await add_user_to_table(conn, r.get('address'), r.get('chainId'), user_uuid)
        return empty()
