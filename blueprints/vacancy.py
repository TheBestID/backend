from json import dumps
from uuid import uuid4, UUID

from eth_utils import to_hex, to_checksum_address
from sanic import Blueprint
from sanic.response import Request, json, empty
from sanic_ext import openapi
from web3 import Web3

from database.users import get_uuid, checkReg
from database.vacancy import clear_database, get_database, edit_vacancy, isAllowed, isCreated, get_owned_vac_by_uuid, \
    get_vacancies_page
from database.vacancy import get_previews_sort_by_int, get_vacancy, get_previews_sort_by_str, delete_vacancy, \
    getUuidByid
from database.vacancy_request import add_vac_request, transfer_to_vacancy
from openapi.vacancy import GetPreviews, GetPreviewsBySTR, GetPreviewsByID, Delete, VacancyEdit, Vacancy, VacancyAdd, \
    GetVacancy
from utils import loadToIpfs, getFromIpfs

vacancy = Blueprint("vacancy", url_prefix="/vacancy")


@vacancy.post("/add_params")
@openapi.body({"application/json": Vacancy}, required=True)
async def add_vacancy_params(request: Request):
    r = request.json
    w3 = request.app.config.get('web3')
    async with request.app.config.get('POOL').acquire() as conn:
        if not await checkReg(conn, r.get('address'), r.get('chainId'), r.get('blockchain')):
            return json({'error': "From wallet isn't registered"}, 409)
        # if not await checkReg(conn, r.get('to_address'), r.get('chainId')):
        #     return json({'error': "To wallet isn't registered"}, 409)

        vac_uuid = uuid4()
        owner_uuid = await get_uuid(conn, r.get('address'), r.get('chainId'), r.get('blockchain'))
        cid = await loadToIpfs(dumps(r.get('data')), request.app.config['account'].key)
        await add_vac_request(conn, vac_uuid, owner_uuid, cid, r.get('price'), r.get('category'))

        data = request.app.config.get('contract_ach').functions.mint(
            [vac_uuid.int, owner_uuid.int, 0, 1, False, cid]).build_transaction(
            {'nonce': w3.eth.get_transaction_count(to_checksum_address(r.get('address'))),
             'from': to_checksum_address(r.get('address'))
             })

        data['value'] = to_hex(data['value'])
        data['gas'] = to_hex(data['gas'])
        data['maxFeePerGas'] = to_hex(data['maxFeePerGas'])
        data['maxPriorityFeePerGas'] = to_hex(data['maxPriorityFeePerGas'])
        data['chainId'] = to_hex(data['chainId'])
        data['nonce'] = to_hex(data['nonce'])

        ####
        # stx = w3.eth.account.signTransaction(data, request.app.config['account'].key)
        # txHash = w3.eth.send_raw_transaction(stx.rawTransaction) 'txHash': str(txHash)
        ###

        return json({'transaction': data, 'sbt_id': vac_uuid.hex})


@vacancy.post("/add")
@openapi.body({"application/json": VacancyAdd}, required=True)
async def add_achievement(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if not await checkReg(conn, r.get('address'), r.get('chainId'), r.get('blockchain')):
            return json({'error': "Wallet isn't registered"}, 409)

        from_uuid = await get_uuid(conn, r.get('address'), r.get('chainId'), r.get('blockchain'))
        trans = await transfer_to_vacancy(conn, r.get('sbt_id'), from_uuid, r.get('txHash'))
        if not trans:
            return json({'error': "SBTid not found"}, 411)
        return json({'uid': 1})


@vacancy.post("/get_owned_vacancy")
@openapi.body({"application/json": GetVacancy}, required=True)
async def get_owned_vacancy(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if not await checkReg(conn, r.get('address'), r.get('chainId'), r.get('blockchain')):
            return json({'error': "From wallet isn't registered"}, 409)

        uuid = await get_uuid(conn, r.get('address'), r.get('chainId'), r.get('blockchain'))
        ach = await get_owned_vac_by_uuid(conn, uuid)
        data = [getFromIpfs(i['cid']) for i in ach]
        return json({'data': data})


@vacancy.post("/get_vacancies")
async def get_vacancies(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_vacancies_page(conn))))


@vacancy.post("/get_vacancy_by_id")
@openapi.body({"application/json": GetPreviewsByID}, required=True)
async def get_preview_by_id(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if not await isCreated(conn, r.get('sbt_id')):
            return empty(409)
        return await get_vacancy(conn, r.get('sbt_id'))


# @vacancy.post("/get_previews_sortby_one")
# @openapi.body({"application/json": GetPreviews}, required=True)
# async def get_previews_sort_by_one(request: Request):
#     async with request.app.config.get('POOL').acquire() as conn:
#         r = request.json
#         return json(list(map(dict, await get_previews_sort_by_int(conn, r.get('sort_value'), r.get('offset_number'),
#                                                                   r.get('top_number'), r.get('in_asc')))))


# @vacancy.post("/get_previews_sortby_two")
# @openapi.body({"application/json": GetPreviewsBySTR}, required=True)
# async def get_previews_sortby_two(request: Request):
#     async with request.app.config.get('POOL').acquire() as conn:
#         r = request.json
#         return json(list(map(dict, await get_previews_sort_by_str(conn, r.get('sort_type1'), r.get('sort_value1'),
#                                                                   r.get('sort_value2'), r.get('offset_number'),
#                                                                   r.get('top_number'), r.get('in_asc')))))


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
                 'from': Web3.toChecksumAddress(r.get('address'))
                 })
            stx = w3.eth.account.signTransaction(tx, request.app.config['account'].key)
            txHash = w3.eth.send_raw_transaction(stx.rawTransaction)
            await delete_vacancy(conn, r.get('id'))
            return empty(200)
        else:
            return empty(409, {'error409': 'No permission to delete vacancy'})
