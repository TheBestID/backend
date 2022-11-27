from uuid import uuid4

from sanic import Blueprint
from sanic.response import Request, json, empty
from sanic_ext import openapi

from database.hacks_request import create_table_hack_request, get_table_hack_request, create_table_hack_request
from database.achievements import create_table_achievements, get_table_achievements
from database.achievements_request import get_table_ach_request, create_table_ach_request
from database.users import create_table_users, get_table_users
from database.vacancy import get_table_vacancy, create_table_vacancy
from database.vacancy_request import get_table_vac_request, create_table_vac_request
from database.verify import create_table_verify, get_table_verify
from database.hacks import get_database
from openapi.user import UserCheck

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


########################################################

@admin.get("/get_bd_verify")
async def get_bd_verify(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_table_verify(conn))))


@admin.get("/clear_bd_verify")
async def clear_bd_verify(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create_table_verify(conn, True)
        return empty()


########################################################

@admin.get("/get_bd_achievements")
async def get_bd_achievements(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_table_achievements(conn))))


@admin.get("/clear_bd_achievements")
async def clear_bd_achievements(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create_table_achievements(conn, True)
        return empty()


########################################################


@admin.get("/get_bd_vacancy")
async def get_bd_vacancy(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_table_vacancy(conn))))


@admin.get("/clear_bd_vacancy")
async def clear_bd_vacancy(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create_table_vacancy(conn, True)
        return empty()


########################################################


@admin.get("/get_bd_vac_request")
async def get_bd_vac_request(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_table_vac_request(conn))))


@admin.get("/clear_bd_vac_request")
async def clear_bd_vac_request(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create_table_vac_request(conn, True)
        return empty()


########################################################

@admin.get("/get_bd_ach_request")
async def get_bd_ach_request(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_table_ach_request(conn))))


@admin.get("/clear_bd_ach_request")
async def clear_bd_ach_request(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create_table_ach_request(conn, True)
        return empty()


########################################################

@admin.get("/get_bd_hack_request")
async def get_bd_ach_request(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_table_hack_request(conn))))


@admin.get("/clear_bd_hack_request")
async def clear_bd_ach_request(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create_table_hack_request(conn, True)
        return empty()


########################################################

@admin.get("/get_bd_hacks")
async def get_bd_ach_request(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_database(conn))))

########################################################


@admin.post("/add_user_test")
@openapi.body({"application/json": UserCheck}, required=True)
async def add_user(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        user_uuid = uuid4()
        await add_user_to_table(conn, r.get('address'), r.get('chainId'), user_uuid)
        return empty()
