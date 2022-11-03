from uuid import uuid4

from sanic import Blueprint
from sanic.response import Request, json, empty
from sanic_ext import openapi
from web3 import Web3

from database.users import check, get_database, clear_database, add_user, get_uuid, reg_user
from database.users import create as create_users
from database.usersinfo import create as create_usersinfo
from database.usersinfo import get_info
from openapi.user import UserAddress, UserAdd, UserCheck

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


@user.get("/get")
async def get_user(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        if not await check(conn, request.json.get('address'), request.json.get('chainId')):
            return json({'error': 'User is not registred'}, 409)

        uuid = await get_uuid(conn, request.json.get('address'), request.json.get('chainId'))
        info = await get_info(conn, uuid)

        return json(dict(info))


@user.post("/msg_params")
@openapi.body({"application/json": UserAddress}, required=True)
async def msg_params(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if await check(conn, r.get('address'), r.get('chainId')):
            return json({'error': 'Wallet is already registered'}, 409)
        uuid = uuid4().hex
        await add_user(conn, r.get('address'), r.get('chainId'), uuid)
    # функция MINT СК
    address = ''
    data: dict = request.app.config['contract'].functions.store(100).build_transaction(
        {'nonce': request.app.config.get('web3').eth.get_transaction_count(
            Web3.toChecksumAddress(request.json.get('address')))})
    data['value'] = Web3.toHex(data['value'])
    data['gas'] = Web3.toHex(data['gas'])
    data['maxFeePerGas'] = Web3.toHex(data['maxFeePerGas'])
    data['maxPriorityFeePerGas'] = Web3.toHex(data['maxPriorityFeePerGas'])
    data['chainId'] = Web3.toHex(data['chainId'])
    data['nonce'] = Web3.toHex(data['nonce'])
    data['uid'] = str(uuid)
    return json(data)


@user.post("/add")
@openapi.body({"application/json": UserAdd}, required=True)
# @openapi.response(200, {"application/json": UserAddressR200}, 'OK')
# @openapi.response(409, description='Wallet is already registered')
async def add(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if await check(conn, r.get('address'), r.get('chainId')):
            return json({'error': 'Wallet is already registered'}, 409)
        await reg_user(conn, r.get('address'), r.get('chainId'))
    return empty(201)


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
        await clear_database(conn)
        return empty()


@user.get("/create_db")
async def create_db(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        await create_usersinfo(conn)
        await create_users(conn)
        return empty()
