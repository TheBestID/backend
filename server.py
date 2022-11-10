from typing import Iterable

from asyncpg import create_pool
from eth_account import Account
from eth_account.signers.local import LocalAccount
from sanic import Sanic
from web3 import Web3

# from blueprints.company import company
from blueprints.user import user
from blueprints.vacancy import vacancy
from blueprints.hacks import hacks
from config import host, password, database, username
from smartcontracts.abi import ABI

app = Sanic("SoulID")

app.config.HEALTH = False

# app.blueprint(company)
app.blueprint(user)
app.blueprint(vacancy)
app.blueprint(hacks)

PK = "cdd47b2a4f9bcce4fda6778f17189640e0fa9b1190f178dc0d335c9012ddf629"


@app.before_server_start
async def init(app1):
    app1.config['POOL'] = await create_pool(host=host, user=username, password=password, database=database, min_size=1,
                                            max_size=1)
    # await create(app1.config['POOL'])
    app1.config['web3'] = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/bbd5ce33856f4a188df9a144746934e4"))
    app1.config['contract'] = app1.config['web3'].eth.contract(address="0x912C9ded9e44BB1aD308560CD1449e28c7735d63",
                                                               abi=ABI)
    app1.config['account']: LocalAccount = Account.from_key(PK)
    app1.config['web3'].eth.default_account = app1.config['account'].address


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
