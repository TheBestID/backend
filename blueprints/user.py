from uuid import uuid4

from eth_utils import to_checksum_address
from sanic import Blueprint
from sanic.response import Request, json, empty
from sanic_ext import openapi

from database.users import check, add_user, reg_user, checkReg, del_users
from database.verify import add_verify, check_verify, del_verify, check_in_verify, update_verify
from openapi.user import UserCheck, GetUser
from smartcontracts import eth, near
from utils import hashing, git_token, send_email

user = Blueprint("user", url_prefix="/user")


@user.post("/check")
@openapi.body({"application/json": UserCheck}, required=True)
async def check_user(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        uid = await checkReg(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''))
        if uid:
            return json({"uuid": uid.hex})
        return empty(409)


@user.post("/get")
@openapi.body({"application/json": GetUser}, required=True)
async def get_user(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        # if await check(conn, r.get('address', ''), r.get('chainId', 0)):
        #     return json({'error': 'User is not registered'}, 409)

        # uuid = await get_uuid(conn, r.get('address', ''), r.get('chainId', 0))
        # #info = await get_info(conn, uuid)
        return json({
            'username': 'username',
            'wallets': [{'chainId': 5, 'address': to_checksum_address('0x41c9288b78090946db0fd6d32D8cB1fEfe18134B')},
                        {'chainId': 4, 'address': to_checksum_address('0x41c9288b78090946db0fd6d32D8cB1fEfe18134B')}]
        })


@user.post("/email")
@openapi.body({"application/json": UserCheck}, required=True)
async def email(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if await check(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')):
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

        if await check_in_verify(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')):
            await update_verify(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''), h_email,
                                e_token.hex, h_g_token)
            return json({"uid": 1})

        await add_verify(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''), h_email, e_token.hex,
                         h_g_token)
        return json({"uid": 1})


@user.post("/msg_params")
@openapi.body({"application/json": UserCheck}, required=True)
async def msg_params(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if await checkReg(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')):
            return json({'error': 'Wallet is already registered'}, 409)
        if not await check_verify(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''),
                                  r.get('hash_email'), r.get('email_token'), r.get('github_token')):
            return json({'error': 'Verification error'}, 408)

        if r.get('blockchain', '').lower() == 'eth':
            if not await check(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')):
                uuid = await eth.mint(request.app.config.get('provider_eth'), request.app.config.get('contract_eth'),
                                      request.app.config.get('account_eth'), r.get('address', ''))
                await add_user(conn, r.get('address', ''), r.get('chainId', 0), uuid, r.get('blockchain', ''))

            transact = await eth.claim(request.app.config.get('provider_eth'), request.app.config.get('contract_eth'),
                                       r.get('address', ''), r.get('hash_email'), r.get('github_token'))
            return json(transact)

        if r.get('blockchain', '').lower() == 'near':
            if not await check(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')):
                uuid = await near.mint(request.app.config.get('contract_near'), request.app.config.get('account_near'),
                                       r.get('address', ''))
                await add_user(conn, r.get('address', ''), r.get('chainId', 0), uuid, r.get('blockchain', ''))

            transact = await near.claim(request.app.config.get('contract_near'), r.get('hash_email')[:32],
                                        r.get('github_token')[:32])
            return json(transact)


@user.post("/add")
@openapi.body({"application/json": UserCheck}, required=True)
async def add(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if not await check(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')):
            return json({'error': "Wallet isn't verified"}, 409)

        uid = await checkReg(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''))
        if uid:
            return json({'error': "Wallet is already verified"}, 408)

        if not await check_in_verify(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')):
            return json({'error': "Wallet isn't verified"}, 411)

        await reg_user(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''))
        await del_verify(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''))

    return json({"uid": uid})


@user.post("/delete_params")
@openapi.body({"application/json": UserCheck}, required=True)
async def delete_params(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        uid = await checkReg(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''))
        if not uid:
            return json({'error': "Wallet isn't registered"}, 409)

        if r.get('blockchain', '').lower() == 'eth':
            transact = await eth.burn(request.app.config.get('provider_eth'), request.app.config.get('contract_eth'),
                                      r.get('address', ''))
            return json(transact)

        if r.get('blockchain', '').lower() == 'near':
            transact = await near.burn(request.app.config.get('contract_near'))
            return json(transact)


@user.post("/delete")
@openapi.body({"application/json": UserCheck}, required=True)
async def delete(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        uid = await checkReg(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''))
        if not uid:
            return json({'error': "Wallet isn't registered"}, 409)
        await del_users(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''))
        return json({'uid': 0})

# @user.post("/test")
# @openapi.body({"application/json": UserCheck}, required=True)
# async def test(request: Request):
#     r = {
#         "hash_email": "0xdc0391e075137f31ce642856bcb62ad2036dc4df31d48d7ca08a7eff3246c7ed",
#         "github_token": "0xb3da07d109597dead06e42475b9dd66b37f11619f8b893d03d78d7be420f2f41"}
#
#     uuid = await near_mint(request.app.config.get('contract_near'), request.app.config.get('account_near'),
#                            'souldev.testnet')
#     transact = await near_claim(request.app.config.get('contract_near'), r.get('hash_email'),
#                                 r.get('github_token'))
#     print(uuid)
#     print(transact)
#     return empty()
