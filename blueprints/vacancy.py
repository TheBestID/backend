from uuid import uuid4

from sanic import Blueprint
from sanic.response import Request, json, empty
from sanic_ext import openapi

from database.vacancy import create, clear_database, get_database, add_vacancy, isAllowed, isCreated
from database.vacancy import get_previews_sort_by_int, get_preview, get_previews_sort_by_str, delete_vacancy

from openapi.vacancy import VacancyTemplate, GetPreviews, GetPreviewsBySTR, GetPreviewsByID, Delete

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
        await add_vacancy(conn, str(r.get('owner_uuid')), r.get('price'), r.get('category'), r.get('timestamp'), r.get('info'))
    return json({"Vacancy is added": 1})



@vacancy.post("/get_previews_sortby_one")
@openapi.body({"application/json": GetPreviews}, required=True)
async def get_previews_sortby_one(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        return json(list(map(dict, await get_previews_sort_by_int(conn, r.get('sort_value'), r.get('offset_number'), r.get('top_number')))))
    return empty(409)


@vacancy.post("/get_previews_sortby_two")
@openapi.body({"application/json": GetPreviewsBySTR}, required=True)
async def get_previews_sortby_two(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        return json(list(map(dict, await get_previews_sort_by_str(conn, r.get('sort_type1'), r.get('sort_value1'), r.get('sort_value2'), r.get('offset_number'), r.get('top_number')))))
    return empty(409)


@vacancy.post("/get_preview_by_id")
@openapi.body({"application/json": GetPreviewsByID}, required=True)
async def get_preview_by_id(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        if await isCreated(conn, r.get('id')):
            return json(list(map(dict, await get_preview(conn,   r.get('id')))))
    return empty(409, {'error': 'no vacancy with such id'})
    
@vacancy.post("/delete_vacancy")
@openapi.body({"application/json": Delete}, required=True)
async def delete_va(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        if await isAllowed(r.get('owner_uuid')) and await isCreated(conn, r.get('id')):
            await delete_vacancy(conn, r.get('id'))
            return empty(200)
        else:
            return empty(409, {'error409': 'No permission to delete'})
            

@vacancy.get("/clear_bd")
async def clear_(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await clear_database(conn)
        return empty()


@vacancy.get("/create_db")
async def create_db(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create(conn, clear=True)
        return empty()

