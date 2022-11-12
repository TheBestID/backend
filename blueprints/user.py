from uuid import uuid4

from eth_utils import to_checksum_address
from eth_utils import to_hex
from sanic import Blueprint
from sanic.response import Request, json, empty
from sanic_ext import openapi

from database.userinfo import get_info
from database.users import check, add_user, get_uuid, reg_user, checkReg
from database.verify import add_verify, check_verify, del_verify, check_in_verify
from openapi.user import UserCheck
from utils import hashing, git_token, send_email

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
        h_email = await hashing(r.get('email'))
        h_g_token = await hashing(g_token)
        em = await send_email(r.get('email'), h_email, h_g_token, e_token, request.app.config.get('email'),
                              request.app.config.get('e_pass'))
        if not em:
            return json({'error': 'Email error'}, 411)
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
    tx = request.app.config.get('contract').functions.mint(to_checksum_address(r.get('address')),
                                                           uuid.int).build_transaction(
        {'nonce': w3.eth.get_transaction_count(request.app.config['account'].address)})
    stx = w3.eth.account.signTransaction(tx, request.app.config['account'].key)
    txHash = w3.eth.send_raw_transaction(stx.rawTransaction)
    w3.eth.wait_for_transaction_receipt(txHash)

    data = request.app.config.get('contract').functions.claim(
        [r.get('hash_email'), r.get('github_token')]).build_transaction(
        {'nonce': w3.eth.get_transaction_count(to_checksum_address(r.get('address')))})

    ###############
    stx = w3.eth.account.signTransaction(data, request.app.config['account'].key)    
    txHash = w3.eth.send_raw_transaction(stx.rawTransaction)
    w3.eth.wait_for_transaction_receipt(txHash)

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
        if await check_in_verify(conn, r.get('address'), r.get('chainId')):
            return json({'error': "Wallet isn't verified"}, 409)
        await reg_user(conn, r.get('address'), r.get('chainId'))
        await del_verify(conn, r.get('address'), r.get('chainId'))
    return json({"uid": 1})

