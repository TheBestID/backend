from typing import Iterable

import near_api
from asyncpg import create_pool
from eth_account import Account as ETH_Account
from eth_account.signers.local import LocalAccount
from near_api.account import Account as NEAR_Account
from near_api.signer import Signer, KeyPair
from sanic import Sanic
from web3 import Web3

from blueprints.achievements import achievements
from blueprints.admin import admin
# from blueprints.company import company
from blueprints.user import user
from blueprints.vacancy import vacancy
from blueprints.hacks import hacks
from config import host, password, database, username
from smartcontracts.abi import ABI, achivement_ABI

app = Sanic("SoulID")

app.config.HEALTH = False

# app.blueprint(company)
app.blueprint(user)
app.blueprint(vacancy)
app.blueprint(hacks)
app.blueprint(admin)
app.blueprint(achievements)

PK_GOERLY = "cdd47b2a4f9bcce4fda6778f17189640e0fa9b1190f178dc0d335c9012ddf629"
PK_NEAR = 'ed25519:2SexAZQWQfuxBuSFKwDzmyPc3YRffZM6khQoLK5XtqpBaBQpMHSGzPJUBtkBX9wpqgnP3zWw9nBeA6o9gyKgdsyD'
signer_id = "souldev.testnet"


@app.before_server_start
async def init(app1):
    app1.config['POOL'] = await create_pool(host=host, user=username, password=password, database=database, min_size=1,
                                            max_size=1)
    # await create(app1.config['POOL'])
    app1.config['web3'] = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/bbd5ce33856f4a188df9a144746934e4"))
    app1.config['contract'] = app1.config['web3'].eth.contract(address="0xC781bB6ccC786823a5A0aD05C01211B09c41beB4",
                                                               abi=ABI)
    app1.config['contract_ach'] = app1.config['web3'].eth.contract(address="0x813F92e52ee1ccFB2222a02C44a718457Dfb6e6F",
                                                                   abi=achivement_ABI)
    app1.config['account']: LocalAccount = ETH_Account.from_key(PK_GOERLY)
    app1.config['web3'].eth.default_account = app1.config['account'].address
    app1.config['email'] = "souldev.web3@gmail.com"
    app1.config['e_pass'] = "zzolvnzkmvkywerq"

    app1.config['near_provider'] = near_api.providers.JsonProvider("https://rpc.testnet.near.org")
    app1.config['near_acc']: NEAR_Account = NEAR_Account(app1.config['near_provider'],
                                                         Signer(signer_id, KeyPair(PK_NEAR)), signer_id)
    app1.config['near_contract'] = "sbt.soul_dev.testnet"


@app.before_server_stop
async def stop(app1):
    app1.config['POOL'].close()


def _add_cors_headers(response, methods: Iterable[str]) -> None:
    allow_methods = list(set(methods))
    if "OPTIONS" not in allow_methods:
        allow_methods.append("OPTIONS")
    headers = {
        "Access-Control-Allow-Methods": ",".join(allow_methods),
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Headers": (
            "origin, content-type, accept, "
            "authorization, x-xsrf-token, x-request-id"
        ),
    }
    response.headers.extend(headers)


def add_cors_headers(request, response):
    if request.method != "OPTIONS":
        methods = [method for method in request.route.methods]
        _add_cors_headers(response, methods)


app.register_middleware(add_cors_headers, "response")

if __name__ == "__main__":
    app.run(dev=True)  # , fast=True
