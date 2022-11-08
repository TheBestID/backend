from uuid import uuid4

from eth_utils import to_checksum_address
from eth_utils import to_hex
from sanic import Blueprint
from sanic.response import Request, json, empty
from sanic_ext import openapi

from database.users import check, get_database, clear_database, add_user, get_uuid, reg_user, checkReg
from database.users import create as create_users
from database.usersinfo import create as create_usersinfo
from database.usersinfo import get_info
from database.verify import add_verify, check_verify, del_verify
from database.verify import create as create_verify
from openapi.user import UserCheck
from utils import hashing, git_token

user = Blueprint("user", url_prefix="/user")


@user.post("/check")
@openapi.body({"application/json": UserCheck}, required=True)
# @openapi.response(200, {"application/json": UserCheck}, description='Wallet is registered')
# @openapi.response(409, description="Wallet isn't registered")
async def check_user(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        if await check(conn, request.json.get('address'), request.json.get('chainId')):
            return json({"uid": 1})
    return empty(409)


@user.post("/get")
@openapi.body({"application/json": UserCheck}, required=True)
async def get_user(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if await check(conn, r.get('address'), r.get('chainId')):
            return json({'error': 'User is not registred'}, 409)

        uuid = await get_uuid(conn, r.get('address'), r.get('chainId'))
        info = await get_info(conn, uuid)
        return json(dict(info))


@user.post("/email")
@openapi.body({"application/json": UserCheck}, required=True)
async def email(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if await check(conn, r.get('address'), r.get('chainId')):
            return json({'error': 'Wallet is already registered'}, 409)
        e_token = uuid4()
        g_token = await git_token(r.get('githubCode'))
        if not g_token:
            return json({'error': 'Github error'}, 408)
        # await send_email(r.get('email'), r.get('githubCode'), e_token)
        h_email = await hashing(r.get('email'))
        h_g_token = await hashing(g_token)
        await add_verify(conn, r.get('address'), r.get('chainId'), h_email, e_token, h_g_token)
        return json({"uid": 1})


@user.post("/msg_params")
@openapi.body({"application/json": UserCheck}, required=True)
async def msg_params(request: Request):
    r = request.json
    w3 = request.app.config.get('web3')
    async with request.app.config.get('POOL').acquire() as conn:
        if await check(conn, r.get('address'), r.get('chainId')):
            return json({'error': 'Wallet is already registered'}, 409)
        if not await check_verify(conn, r.get('address'), r.get('chainId'), r.get('hash_email'), r.get('email_token'),
                                  r.get('github_token')):
            return json({'error': 'Verification error'}, 408)
        uuid = uuid4()
        await add_user(conn, r.get('address'), r.get('chainId'), uuid)
    tx = request.app.config.get('contract').functions.mint(uuid.hex).build_transaction(
        {'nonce': w3.eth.get_transaction_count(request.app.config['account'].address)})
    stx = w3.eth.account.signTransaction(tx, request.app.config['account'].key)
    txHash = w3.eth.send_raw_transaction(stx.rawTransaction)

    data = request.app.config.get('contract').functions.claim(to_checksum_address(r.get('address')), uuid,
                                                              [r.get('hash_email'),
                                                               r.get('github_token')]).build_transaction(
        {'nonce': w3.eth.get_transaction_count(to_checksum_address(r.get('address')))})
    data['value'] = to_hex(data['value'])
    data['gas'] = to_hex(data['gas'])
    data['maxFeePerGas'] = to_hex(data['maxFeePerGas'])
    data['maxPriorityFeePerGas'] = to_hex(data['maxPriorityFeePerGas'])
    data['chainId'] = to_hex(data['chainId'])
    data['nonce'] = to_hex(data['nonce'])
    return json(data)


@user.post("/add")
@openapi.body({"application/json": UserCheck}, required=True)
# @openapi.response(200, {"application/json": UserAddressR200}, 'OK')
# @openapi.response(409, description='Wallet is already registered')
async def add(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if not await check(conn, r.get('address'), r.get('chainId')):
            return json({'error': "Wallet isn't verified"}, 409)
        if await checkReg(conn, r.get('address'), r.get('chainId')):
            return json({'error': "Wallet is already verified"}, 408)
        await reg_user(conn, r.get('address'), r.get('chainId'))
        await del_verify(conn, r.get('address'), r.get('chainId'))
    return json({"uid": 1})


# @user.post("/email")
# @openapi.body({"application/json": UserEmail}, required=True)
# @openapi.response(200, {"application/json": UserEmailR200}, 'OK')
# @openapi.response(409, description="Wallet isn't registered")
# async def add_email(request: Request):
#     r = request.json
#     async with request.app.config.get('POOL').acquire() as conn:
#         res = await check_github(conn, request.json.get('address'))
#         if not res:
#             return json({'error': "Wallet isn't registered"}, 409)
#         await insert_email(conn, r.get('email'), r.get('address'))
#
#         sbt = await send_data({"uid": res[0], "github": res[1], "email": r.get('email'),
#                                "address": r.get('address')})  # получение sbt от смарт-контракта
#     return json({'sbt': sbt})


@user.get("/get_bd")
async def get_bd(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_database(conn))))


@user.get("/clear_bd")
async def clear_(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create_usersinfo(conn, True)
        await create_users(conn, True)
        await create_verify(conn, True)
        return empty()


@user.get("/create_db")
async def create_db(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create_usersinfo(conn)
        await create_users(conn)
        await create_verify(conn)
        return empty()
