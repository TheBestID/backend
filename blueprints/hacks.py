from sanic import Blueprint
from sanic.response import Request, json, empty
from sanic_ext import openapi

from database.hacks import get_database, create, clear_database, isAllowed_, isCreated_, add_hack, get_hack
from database.hacks import get_previews_sort_by_int, get_previews_sort_by_str
from openapi.hacks import AddHack, SortByInt, SortByStr, GetById
from database.users import get_uuid
hacks = Blueprint("hacks", url_prefix="/hacks")


@hacks.get("/get_bd")
async def get_bd(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_database(conn))))


@hacks.post("/add")
@openapi.body({"application/json": AddHack}, required=True)
async def add(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        # if await check(conn, r.get('address'), r.get('chaiId')) == True:
        if isAllowed_():
            # add work with
            await add_hack(conn, await get_uuid(conn, r.get('address'), r.get('chainId'), r.get('blockchain')), r.get('theme'), r.get('base_color'), r.get('font_head'),
                           r.get('font_par'),
                           r.get('hackathon_name'), r.get('description'), r.get('back_url'), r.get('logo_url'),
                           r.get('price'),
                           r.get('pool'), r.get('descr_price'), r.get('sbt_url'), r.get('descr_price'),
                           r.get('social_link'), r.get('category'))
            return empty(200)
        else:
            return empty(409, {'eror': 'No permissions'})


@hacks.post("/get_previews_sortby_one")
@openapi.body({"application/json": SortByInt}, required=True)
async def get_previews_sortby_one(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        return json(list(map(dict, await get_previews_sort_by_int(conn, r.get('sort_value'), r.get('offset_number'),
                                                                  r.get('top_number'), r.get('in_asc')))))


@hacks.post("/get_previews_sortby_two")
@openapi.body({"application/json": SortByStr}, required=True)
async def get_previews_sortby_two(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        return json(list(map(dict, await get_previews_sort_by_str(conn, r.get('sort_type'), r.get('sort_value'),
                                                                  r.get('sort_value_int'), r.get('offset_number'),
                                                                  r.get('top_number'), r.get('in_asc')))))


@hacks.post("/get_hack_by_id")
@openapi.body({"application/json": GetById}, required=True)
async def get_preview_by_id(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        if await isCreated_(conn, r.get('id')):
            return json(list(map(dict, await get_hack(conn, r.get('id')))))
    return empty(409, {'error': 'no vacancy with such id'})


@hacks.get("/clear_bd")
async def clear_(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await clear_database(conn)
        return empty()


@hacks.get("/create_db")
async def create_db(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create(conn, clear=True)
        return empty()
