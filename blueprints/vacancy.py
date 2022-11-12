from uuid import uuid4

from sanic import Blueprint
from sanic.response import Request, json, empty
from sanic_ext import openapi

from database.users import check, get_uuid
from database.vacancy import create, clear_database, get_database, add_vacancy, edit_vacancy, isAllowed, isCreated
from database.vacancy import get_previews_sort_by_int, get_vacancy, get_previews_sort_by_str, delete_vacancy, getUuidByid


from openapi.vacancy import VacancyAdd, GetPreviews, GetPreviewsBySTR, GetPreviewsByID, Delete, VacancyEdit, Confirm


vacancy = Blueprint("vacancy", url_prefix="/vacancy")


@vacancy.get("/get_bd")
async def get_bd(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_database(conn))))


@vacancy.post("/add")
@openapi.body({"application/json": VacancyAdd}, required=True)
async def add(request: Request):
    r = request.json
    w3 = request.app.config.get('web3')
    async with request.app.config.get('POOL').acquire() as conn:
        if await check(conn, r.get('address'), str(r.get('chainId'))):
            
            ach_uuid = uuid4()
            int_uuid = (await get_uuid(conn, r.get('address'), r.get('chainId'))).int

            cid = await add_vacancy(conn, str(await get_uuid(conn, r.get('address'), r.get('chainId'))), r.get('price'), r.get('category'), r.get('info'), str(ach_uuid))

            data = request.app.config.get('contract_ach').functions.mint([ach_uuid.int, int_uuid, 0, 1, False, cid]).build_transaction(
            {'nonce': w3.eth.get_transaction_count(request.app.config['account'].address)
            })

            if r.get('return_trans'):
                data['value'] = to_hex(data['value'])
                data['gas'] = to_hex(data['gas'])
                data['maxFeePerGas'] = to_hex(data['maxFeePerGas'])
                data['maxPriorityFeePerGas'] = to_hex(data['maxPriorityFeePerGas'])
                data['chainId'] = to_hex(data['chainId'])
                data['nonce'] = to_hex(data['nonce'])
                return json(data)
            else:
                stx = w3.eth.account.signTransaction(tx, request.app.config['account'].key)
                txHash = w3.eth.send_raw_transaction(stx.rawTransaction)
                #w3.eth.wait_for_transaction_receipt(txHash)
            return empty(200)
        else:
            return empty(409, {'eror': 'No permissions'})


@vacancy.post("/get_previews_sortby_one")
@openapi.body({"application/json": GetPreviews}, required=True)
async def get_previews_sortby_one(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        return json(list(map(dict, await get_previews_sort_by_int(conn, r.get('sort_value'), r.get('offset_number'),
                                                                  r.get('top_number'), r.get('in_asc')))))


@vacancy.post("/get_previews_sortby_two")
@openapi.body({"application/json": GetPreviewsBySTR}, required=True)
async def get_previews_sortby_two(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        return json(list(map(dict, await get_previews_sort_by_str(conn, r.get('sort_type1'), r.get('sort_value1'),
                                                                  r.get('sort_value2'), r.get('offset_number'),
                                                                  r.get('top_number'), r.get('in_asc')))))


@vacancy.post("/get_vacancy_by_id")
@openapi.body({"application/json": GetPreviewsByID}, required=True)
async def get_preview_by_id(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        if await isCreated(conn, r.get('id')):
            return await get_vacancy(conn, r.get('id'))
    return empty(409, {'error': 'no vacancy with such id'})


@vacancy.post("/edit_vacancy")
@openapi.body({"application/json": VacancyEdit}, required=True)
async def edit_va(request: Request):
    # claim sbt!
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


@vacancy.post("/confirm_vacancy")
@openapi.body({"application/json": Confirm}, required=True)
async def confirm_vacancy(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if r.get('hash') != '':
            return empty(200)
        else:
            await delete_vacancy(r.get('id'))
        pass


@vacancy.post("/delete_vacancy")
@openapi.body({"application/json": Delete}, required=True)
async def delete_va(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        r = request.json
        w3 = request.app.config.get('web3')
        uuid_sender = await get_uuid(conn, r.get('address'), str(r.get('chainId')))
        if uuid_sender:
            uuid_sender = str(uuid_sender)
        else:
            return empty(409, {'error409': 'No such registred user'})

        if not await isCreated(conn, r.get('id')):
             return empty(409, {'error409': 'No such vacancy'})
        if await isAllowed(conn, uuid_sender, r.get('id')):
            
            ach_uuid = UUID(await getUuidByid(conn, r.get('id')))
            tx = request.app.config.get('contract_ach').functions.burn(ach_uuid.int).build_transaction(
            {'nonce': w3.eth.get_transaction_count(request.app.config['account'].address),
             'from': request.app.config['account'].address
            })
            stx = w3.eth.account.signTransaction(tx, request.app.config['account'].key)
            txHash = w3.eth.send_raw_transaction(stx.rawTransaction)
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
