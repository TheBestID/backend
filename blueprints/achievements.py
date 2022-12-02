from json import dumps
from uuid import uuid4

from sanic import Blueprint
from sanic.request import File
from sanic.response import Request, json
from sanic_ext import openapi
from sanic_ext.extensions.openapi.definitions import RequestBody

from database.achievements import get_owned_ach_by_uuid, get_created_ach_by_uuid
from database.achievements_request import add_ach_request, transfer_to_achievements
from database.users import get_uuid, checkReg, checkReg_by_uid
from openapi.achievement import Achievement, GetAchievement, AchievementAdd
from smartcontracts import eth, near
from utils import loadToIpfs, getFromIpfs, loadFile

achievements = Blueprint("achievements", url_prefix="/achievements")


@achievements.post("/add_params")
@openapi.body(RequestBody({"multipart/form-data": Achievement}))
async def add_achievement_params(request: Request):
    r = request.form
    print(r)
    image: File = request.files.get('image')

    async with request.app.config.get('POOL').acquire() as conn:
        from_uuid = await checkReg(conn, r.get('from_address'), r.get('chainId'), r.get('blockchain'))
        if not from_uuid:
            return json({'error': "From wallet isn't registered"}, 409)

        to_uuid = await checkReg(conn, r.get('to_address'), r.get('chainId'), r.get('blockchain'))
        if not to_uuid:
            return json({'error': "From wallet isn't registered"}, 409)

        ach_type = 0
        verifier = uuid4()

        data = r.get('data')
        if image:
            image_cid = await loadFile(image)
            data['image_cid'] = image_cid
        cid = await loadToIpfs(dumps(data), request.app.config['account_eth'].key)

        if r.get('blockchain', '').lower() == 'eth':
            ach_uuid, transact = await eth.mint_achievement(request.app.config.get('provider_eth'),
                                                            request.app.config.get('contract_ach_eth'),
                                                            ach_type, r.get('from_address'), from_uuid, to_uuid,
                                                            verifier,
                                                            cid, 0)

        if r.get('blockchain', '').lower() == 'near':
            ach_uuid, transact = await near.mint_achievement()

        await add_ach_request(conn, ach_uuid, from_uuid, to_uuid, cid, image_cid, ach_type)

        return json({'transaction': transact, 'sbt_id': ach_uuid.hex})


@achievements.post("/add")
@openapi.body({"application/json": AchievementAdd}, required=True)
async def add_achievement(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        from_uuid = await checkReg(conn, r.get('address'), r.get('chainId'), r.get('blockchain'))
        if not from_uuid:
            return json({'error': "From wallet isn't registered"}, 409)

        trans = await transfer_to_achievements(conn, r.get('sbt_id'), from_uuid, r.get('txHash'))
        if not trans:
            return json({'error': "SBTid not found"}, 411)
        return json({'uid': from_uuid.hex})


@achievements.post("/get_owned_achievement")
@openapi.body({"application/json": GetAchievement}, required=True)
async def get_owned_achievement(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if not await checkReg_by_uid(conn, r.get('uid')):
            return json({'error': "From wallet isn't registered"}, 409)

        # data = request.app.config.get('contract_ach_eth').functions.getAchievementsOfOwner(
        #     to_checksum_address("0x41c9288b78090946db0fd6d32d8cb1fefe18134b")).call()
        # print(data)
        ach = await get_owned_ach_by_uuid(conn, r.get('uid'))
        data = [getFromIpfs(i['cid']) for i in ach]
        return json({'data': data})


@achievements.post("/get_created_achievement")
@openapi.body({"application/json": GetAchievement}, required=True)
async def get_created_achievement(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if not await checkReg(conn, r.get('address'), r.get('chainId'), r.get('blockchain')):
            return json({'error': "From wallet isn't registered"}, 409)

        uuid = await get_uuid(conn, r.get('address'), r.get('chainId'), r.get('blockchain'))
        ach = await get_created_ach_by_uuid(conn, uuid)
        data = [getFromIpfs(i['cid']) for i in ach]
        return json({'data': data})
