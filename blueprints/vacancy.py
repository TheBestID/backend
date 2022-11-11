from uuid import uuid4

from sanic import Blueprint
from sanic.response import Request, json, empty
from sanic_ext import openapi

from database.vacancy import create, clear_database, get_database, add_vacancy, edit_vacancy, isAllowed, isCreated
from database.vacancy import get_previews_sort_by_int, get_vacancy, get_previews_sort_by_str, delete_vacancy
from database.users  import check, get_uuid

from openapi.vacancy import VacancyTemplate, VacancyAdd, GetPreviews, GetPreviewsBySTR, GetPreviewsByID, Delete, VacancyEdit

vacancy = Blueprint("vacancy", url_prefix="/vacancy")

@vacancy.get("/get_bd")
async def get_bd(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_database(conn))))



@vacancy.post("/add")
@openapi.body({"application/json": VacancyAdd}, required=True)
# @openapi.response(200, {"application/json": UserAddressR200}, 'OK')
# @openapi.response(409, description='Wallet is already registered')
async def add(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if await check(conn, r.get('address'), str(r.get('chainId'))) == True:
            await add_vacancy(conn, str(await get_uuid(conn, r.get('address'), str(r.get('chainId')))), r.get('price'), r.get('category'), r.get('info'))
            return empty(200)
        else:
           return empty(409, {'eror': 'No permissions' })



@vacancy.post("/get_previews_sortby_one")
@openapi.body({"application/json": GetPreviews}, required=True)
async def get_previews_sortby_one(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        return json(list(map(dict, await get_previews_sort_by_int(conn, r.get('sort_value'), r.get('offset_number'), r.get('top_number'), r.get('in_asc')))))
    return empty(409)


@vacancy.post("/get_previews_sortby_two")
@openapi.body({"application/json": GetPreviewsBySTR}, required=True)
async def get_previews_sortby_two(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        return json(list(map(dict, await get_previews_sort_by_str(conn, r.get('sort_type1'), r.get('sort_value1'), r.get('sort_value2'), r.get('offset_number'), r.get('top_number'), r.get('in_asc')))))
    return empty(409)


@vacancy.post("/get_vacancy_by_id")
@openapi.body({"application/json": GetPreviewsByID}, required=True)
async def get_preview_by_id(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        if await isCreated(conn, r.get('id')):
            return await get_vacancy(conn, r.get('id'))
            #return json(list(map(dict, await get_vacancy(conn,   r.get('id')))))
    return empty(409, {'error': 'no vacancy with such id'})
    

@vacancy.post("/edit_vacancy")
@openapi.body({"application/json": VacancyEdit}, required=True)
async def edit_va(request: Request):
    #claim sbt!
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        
        uuid_sender = await get_uuid(conn, r.get('address'), str(r.get('chainId')))
        if uuid_sender:
            uuid_sender = str(uuid_sender)
        else:
            return empty(409, {'error409': 'No such registred user'})

        if not await isCreated(conn, r.get('id')):
             return empty(409, {'error409': 'No such vacancy'})

        if await isAllowed(conn, uuid_sender, r.get('id')):
            await edit_vacancy(conn, r.get('id'), r.get('price'), r.get('category'), r.get('info'), uuid_sender)
            return empty(200)
        else:
            return empty(409, {'error409': 'No permission to edit vacancy'})


@vacancy.post("/delete_vacancy")
@openapi.body({"application/json": Delete}, required=True)
async def delete_va(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        
        
        uuid_sender = await get_uuid(conn, r.get('address'), str(r.get('chainId')))
        if uuid_sender:
            uuid_sender = str(uuid_sender)
        else:
            return empty(409, {'error409': 'No such registred user'})

        if not await isCreated(conn, r.get('id')):
             return empty(409, {'error409': 'No such vacancy'})


        if await isAllowed(conn, uuid_sender, r.get('id')):
             await delete_vacancy(conn, r.get('id'))
             return empty(200)
        else:
             return empty(409, {'error409': 'No permission to delete vacancy'})
            

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

