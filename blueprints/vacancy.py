from uuid import uuid4

from sanic import Blueprint
from sanic.response import Request, json, empty
from sanic_ext import openapi

from database.vacancy import create, clear_database, get_database, add_vacancy
from openapi.vacancy import VacancyTemplate

vacancy = Blueprint("vacancy", url_prefix="/vacancy")

@vacancy.get("/get_bd")
async def get_bd(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_database(conn))))



@vacancy.post("/add")
@openapi.body({"application/json": VacancyTemplate}, required=True)
# @openapi.response(200, {"application/json": UserAddressR200}, 'OK')
# @openapi.response(409, description='Wallet is already registered')
async def add(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        await add_vacancy(conn, r.get('id'), r.get('owner_uuid'), r.get('price'), r.get('category'), r.get('timestamp'), r.get('info'))
    return json({"uuid": 1})


@vacancy.get("/clear_bd")
async def clear_(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await clear_database(conn)
        return empty()


@vacancy.get("/create_db")
async def create_db(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create(conn)
        return empty()