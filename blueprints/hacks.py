from sanic import Blueprint
from sanic.response import Request, json, empty
from sanic_ext import openapi
from uuid import uuid4

from database.hacks_request import add_hack_request, transfer_to_hacks
from database.hacks import get_database, create, clear_database, isAllowed_, isCreated_, add_hack, get_hack
from database.hacks import get_previews_sort_by_int, get_previews_sort_by_str
from openapi.hacks import AddHack, SortByInt, SortByStr, GetById, AddHack_last
from database.users import get_uuid

hacks = Blueprint("hacks", url_prefix="/hacks")


@hacks.get("/get_bd")
async def get_bd(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_database(conn))))


@hacks.post("/add_params")
@openapi.body({"application/json": AddHack}, required=True)
async def add_params(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        # if await check(conn, r.get('address'), r.get('chaiId')) == True:
        if isAllowed_():
            # add work with
            hack_uuid = uuid4()
            await add_hack_request(conn, hack_uuid,
                                   await get_uuid(conn, r.get('address'), r.get('chainId'), r.get('blockchain')),
                                   r.get('theme'), r.get('base_color'), r.get('font_head'),
                                   r.get('font_par'),
                                   r.get('hackathon_name'), r.get('description'), r.get('back_url'), r.get('logo_url'),
                                   r.get('price'),
                                   r.get('pool'), r.get('descr_price'), r.get('sbt_url'), r.get('descr_price'),
                                   r.get('social_link'), r.get('category'), r.get('start_date'), r.get('end_date'))

            return json({'transaction': 'trans', 'hack_id': hack_uuid.hex})
        else:
            return empty(409, {'eror': 'No permissions'})


@hacks.post("/add")
@openapi.body({"application/json": AddHack_last}, required=True)
async def add_hack(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if isAllowed_():
            from_uuid = await get_uuid(conn, r.get('address'), r.get('chainId'), r.get('blockchain'))
            trans = await transfer_to_hacks(conn, r.get('hack_id'), from_uuid, r.get('txHash'))
            if not trans:
                return json({'error': "SBTid not found"}, 411)
            return json({'uid': 1})


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
