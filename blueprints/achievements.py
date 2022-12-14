from json import loads
from uuid import uuid4

from sanic import Blueprint
from sanic.request import File
from sanic.response import Request, json
from sanic_ext import openapi
from sanic_ext.extensions.openapi.definitions import RequestBody

from database.achievements import get_owned_ach_by_uuid
from database.achievements_request import add_ach_request, transfer_to_achievements
from database.users import checkReg, checkReg_by_uid
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

    def get_type(data: dict):
        if data.get('company') == '' and data.get('position') == '':
            if data.get('description') == 'profile':
                return 0
            if data.get('description') == 'background':
                return 1
        return 3

    async with request.app.config.get('POOL').acquire() as conn:
        from_uuid = await checkReg(conn, r.get('from_address'), r.get('chainId'), r.get('blockchain'))
        if not from_uuid:
            return json({'error': "From wallet isn't registered"}, 409)

        to_uuid = await checkReg(conn, r.get('to_address'), r.get('chainId'), r.get('blockchain'))
        if not to_uuid:
            return json({'error': "From wallet isn't registered"}, 410)

        ach_type = get_type(loads(r.get('data')))
        print(ach_type)
        verifier = uuid4()

        cid = await loadToIpfs(r.get('data'), request.app.config['account_eth'].key)

        if r.get('blockchain', '').lower() == 'eth':
            ach_uuid, transact = await eth.mint_achievement(request.app.config.get('provider_eth'),
                                                            request.app.config.get('contract_ach_eth'),
                                                            ach_type, r.get('from_address'), from_uuid, to_uuid,
                                                            verifier,
                                                            cid, 0)

        if r.get('blockchain', '').lower() == 'near':
            ach_uuid, transact = await near.mint_achievement()

        if image:
            image_cid = await loadFile(image)
            await add_ach_request(conn, ach_uuid, from_uuid, to_uuid, cid, image_cid, ach_type)
        else:
            await add_ach_request(conn, ach_uuid, from_uuid, to_uuid, cid, 'None', ach_type)

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

        def getInfo(cid, image_cid):
            _data = getFromIpfs(cid)
            _data['image_cid'] = image_cid
            return _data

        # data = request.app.config.get('contract_ach_eth').functions.getAchievementsOfOwner(
        #     to_checksum_address("0x41c9288b78090946db0fd6d32d8cb1fefe18134b")).call()
        # print(data)
        ach = await get_owned_ach_by_uuid(conn, r.get('uid'))
        data = [getInfo(i['cid'], i['image_cid']) for i in ach]
        return json({'data': data})

# @achievements.post("/get_created_achievement")
# @openapi.body({"application/json": GetAchievement}, required=True)
# async def get_created_achievement(request: Request):
#     r = request.json
#     async with request.app.config.get('POOL').acquire() as conn:
#         if not await checkReg(conn, r.get('address'), r.get('chainId'), r.get('blockchain')):
#             return json({'error': "From wallet isn't registered"}, 409)
#
#         uuid = await get_uuid(conn, r.get('address'), r.get('chainId'), r.get('blockchain'))
#         ach = await get_created_ach_by_uuid(conn, uuid)
#         data = [getFromIpfs(i['cid']) for i in ach]
#         return json({'data': data})
