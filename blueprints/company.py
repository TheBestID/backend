from sanic import Blueprint
from sanic.response import Request, text
from sanic.response import json, empty
from uuid import UUID, uuid4
from utils import hashing, git_token, send_email

from openapi.company import CompanyTemplate, CompanyEmail, CompanyAdd, CompanyMsgParams
from sanic_ext import openapi

from database.users import check, add_user, reg_user, checkReg, del_users
from database.company import check_company, check_link, add_company
from database.company import checkReg_by_uid_Comp, checkRegComp, reg_company
from database.company_request import transfer_to_company, add_req, del_comp_req, check_company_req
from database.verify import add_verify, check_verify, del_verify, check_in_verify, update_verify, check_verify_company
from smartcontracts import eth, near

company = Blueprint("company", url_prefix="/company")


@company.post("/create")
async def create_company(request: Request):
    return text("Done.")


@company.get("/")
async def get_company(request: Request):
    return text("Company #1.")



@company.post("/email")
@openapi.body({"application/json": CompanyEmail}, required=True)
async def email(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if await check(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')) or await check_company(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')):
            return json({'error': 'Wallet is already registered'}, 409)
        
        if not await check_link(r.get('link'), r.get('email')):
            return json({'error': 'Not allowed domain'}, 409)

        e_token = uuid4()
        g_token = await git_token(r.get('githubCode'))
        if not g_token:
            return json({'error': 'Github error'}, 408)
        h_email = await hashing(r.get('email'))
        email = r.get('email')
        h_g_token = await hashing(g_token)
        em = await send_email(r.get('email'), h_email, h_g_token, e_token, request.app.config.get('email'),
                              request.app.config.get('e_pass'))
        if not em:
            return json({'error': 'Email error'}, 411)

        await add_req(conn, r.get('address'), r.get('chainId'), r.get('blockchain'), r.get('link'), r.get('email'))

        if await check_in_verify(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')):
            await update_verify(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''), h_email,
                                e_token.hex, h_g_token)
            return json({"uid": 1})

        await add_verify(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''), email, e_token.hex,
                         h_g_token)
        return json({"uid": 1})


@company.post("/msg_params")
@openapi.body({"application/json": CompanyMsgParams}, required=True)
async def msg_params(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:

        if await checkReg(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')) or await checkRegComp(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')):
            return json({'error': 'Wallet is already registered'}, 409)
        if not await check_verify_company(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''),
                                  r.get('email_token'), r.get('github_token')):
            return json({'error': 'Verification error'}, 408)
        uuid = uuid4()
        await transfer_to_company(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''), uuid)
        return json({'transact': 'transact'})

        if r.get('blockchain', '').lower() == 'eth':
            if not await check_company(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')):
                uuid = await eth.mint(request.app.config.get('provider_eth'), request.app.config.get('contract_eth'),
                                      request.app.config.get('account_eth'), r.get('address', ''))
                await transfer_to_company(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''), uuid)

            transact = await eth.claim(request.app.config.get('provider_eth'), request.app.config.get('contract_eth'),
                                       r.get('address', ''), r.get('hash_email'), r.get('github_token'))
            return json(transact)

        if r.get('blockchain', '').lower() == 'near':
            if not await check_company(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')):
                uuid = await near.mint(request.app.config.get('contract_near'), request.app.config.get('account_near'),
                                       r.get('address', ''))
                await transfer_to_company(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''), uuid)

            transact = await near.claim(request.app.config.get('contract_near'), r.get('hash_email')[:32],
                                        r.get('github_token')[:32])
            return json(transact)


@company.post("/add")
@openapi.body({"application/json": CompanyAdd}, required=True)
async def add(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if not await check_company(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')):
             return json({'error': "Wallet isn't verified"}, 409)

        uid = await checkRegComp(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''))
        if uid:
            return json({'error': "Wallet is already verified"}, 408)

        if not await check_in_verify(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', '')):
            return json({'error': "Wallet isn't verified"}, 411)

        await reg_company(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''))
        await del_verify(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''))
        await del_comp_req(conn, r.get('address', ''), r.get('chainId', 0), r.get('blockchain', ''))


    return json({"uid": uid})