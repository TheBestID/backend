from json import dumps
from uuid import uuid4

from eth_utils import to_checksum_address
from eth_utils import to_hex
from sanic import Blueprint
from sanic.response import Request, json
from sanic_ext import openapi

from database.achievements import get_owned_ach_by_uuid, get_created_ach_by_uuid
from database.achievements_request import add_ach_request, transfer_to_achievements
from database.users import get_uuid, checkReg
from openapi.achievement import Achievement, GetAchievement, AchievementAdd
from utils import loadToIpfs, getFromIpfs

achievements = Blueprint("achievements", url_prefix="/achievements")


@achievements.post("/add_params")
@openapi.body({"application/json": Achievement}, required=True)
async def add_achievement_params(request: Request):
    r = request.json
    w3 = request.app.config.get('web3')
    async with request.app.config.get('POOL').acquire() as conn:
        if not await checkReg(conn, r.get('from_address'), r.get('chainId')):
            return json({'error': "From wallet isn't registered"}, 409)
        if not await checkReg(conn, r.get('to_address'), r.get('chainId')):
            return json({'error': "To wallet isn't registered"}, 409)

        ach_uuid = uuid4()
        from_uuid = await get_uuid(conn, r.get('from_address'), r.get('chainId'))
        to_uuid = await get_uuid(conn, r.get('to_address'), r.get('chainId'))
        ach_type = ''
        verifier = 0
        cid = await loadToIpfs(dumps(r.get('data')), request.app.config['account'].key)
        await add_ach_request(conn, ach_uuid, from_uuid, to_uuid, cid, ach_type)

        data = request.app.config.get('contract_ach').functions.mint(
            [ach_uuid.int, from_uuid.int, to_uuid.int, verifier, False, cid]).build_transaction(
            {'nonce': w3.eth.get_transaction_count(to_checksum_address(r.get('from_address'))),
             'from': to_checksum_address(r.get('from_address'))
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

        return json({'transaction': data, 'sbt_id': ach_uuid.hex})


@achievements.post("/add")
@openapi.body({"application/json": AchievementAdd}, required=True)
async def add_achievement(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if not await checkReg(conn, r.get('address'), r.get('chainId')):
            return json({'error': "Wallet isn't registered"}, 409)

        from_uuid = await get_uuid(conn, r.get('address'), r.get('chainId'))
        trans = await transfer_to_achievements(conn, r.get('sbt_id'), from_uuid, r.get('txHash'))
        if not trans:
            return json({'error': "SBTid not found"}, 411)
        return json({'uid': 1})


@achievements.post("/get_owned_achievement")
@openapi.body({"application/json": GetAchievement}, required=True)
async def get_owned_achievement(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if not await checkReg(conn, r.get('address'), r.get('chainId')):
            return json({'error': "From wallet isn't registered"}, 409)

        uuid = await get_uuid(conn, r.get('address'), r.get('chainId'))
        ach = await get_owned_ach_by_uuid(conn, uuid)
        data = [getFromIpfs(i['cid']) for i in ach]
        return json({'data': data})


@achievements.post("/get_created_achievement")
@openapi.body({"application/json": GetAchievement}, required=True)
async def get_created_achievement(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if not await checkReg(conn, r.get('address'), r.get('chainId')):
            return json({'error': "From wallet isn't registered"}, 409)

        uuid = await get_uuid(conn, r.get('address'), r.get('chainId'))
        ach = await get_created_ach_by_uuid(conn, uuid)
        data = [getFromIpfs(i['cid']) for i in ach]
        return json({'data': data})
