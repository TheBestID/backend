from sanic import Blueprint
from sanic.response import Request, json, empty
from sanic_ext import openapi

from smartcontracts.conn_to_sol import send_data, get_data
from openapi.user import UserAddress, UserAddressR200, UserEmail, UserEmailR200, UserCheck
from database.table import insert_address, insert_email, check_address, check_github, get_database

user = Blueprint("user", url_prefix="/user")


@user.post("/check")
@openapi.body({"application/json": UserAddress}, required=True)
@openapi.response(200, {"application/json": UserCheck}, description='Wallet is registered')
@openapi.response(409, description="Wallet isn't registered")
async def check_user(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        if await check_address(conn, r.get('address')):
            data = await get_data(r.get('address'))
            return json(data)
    return empty(409)


@user.post("/address")
@openapi.body({"application/json": UserAddress}, required=True)
@openapi.response(200, {"application/json": UserAddressR200}, 'OK')
@openapi.response(409, description='Wallet is already registered')
async def add_address(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        if await check_address(conn, request.json.get('address')):
            return json({'error': 'Wallet is already registered'}, 409)
        uid = await insert_address(conn, request.json.get('address'))
    return json({'uid': uid})


@user.post("/email")
@openapi.body({"application/json": UserEmail}, required=True)
@openapi.response(200, {"application/json": UserEmailR200}, 'OK')
@openapi.response(409, description="Wallet isn't registered")
async def add_email(request: Request):
    r = request.json
    async with request.app.config.get('POOL').acquire() as conn:
        res = await check_github(conn, request.json.get('address'))
        if not res:
            return json({'error': "Wallet isn't registered"}, 409)
        await insert_email(conn, r.get('email'), r.get('address'))

        sbt = await send_data({"uid": res[0], "github": res[1], "email": r.get('email'),
                               "address": r.get('address')})  # получение sbt от смарт-контракта
    return json({'sbt': sbt})


@user.get("/get_bd")
async def get_bd(request: Request):
    async with request.app.config.get('POOL').acquire() as conn:
        return json(list(map(dict, await get_database(conn))))
