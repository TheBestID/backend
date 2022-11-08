import asyncio
from uuid import uuid4
import hashlib

from bcrypt import hashpw, gensalt
from web3 import Web3
from web3.eth import AsyncEth

from smartcontracts.abi import ABI
import time

from web3.middleware import construct_sign_and_send_raw_middleware

from eth_account import Account
from eth_account.signers.local import LocalAccount


def send_data():
    w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/bbd5ce33856f4a188df9a144746934e4"))
    myContract = w3.eth.contract(address="0x675Cb077282d22eF8B25A02ed279B8fb50da7769", abi=ABI)
    w3.eth.default_account = '0x41c9288b78090946db0fd6d32D8cB1fEfe18134B'
    pk = "cdd47b2a4f9bcce4fda6778f17189640e0fa9b1190f178dc0d335c9012ddf629"
    print(w3.eth.default_account)
    uuid = uuid4()
    url = Web3.toHex(b'url tester')
    git = Web3.toHex(b'git_tester')
    eml = Web3.toHex(b'email tester')
    hsh = myContract.functions.mint(
        w3.toChecksumAddress('0x9a56A3492d13E26E9C56B4Be3E30918e5F551684'), 1,
        [url, git, eml]).build_transaction({'nonce': w3.eth.get_transaction_count(w3.eth.default_account)})
    shsh = w3.eth.account.signTransaction(hsh, pk)
    tx = w3.eth.send_raw_transaction(shsh.rawTransaction)
    return '1'


# тест 0x65a8ba2F8F301d95196ec669590631aA615f2c95
send_data()
# account: LocalAccount = Account.from_key("cdd47b2a4f9bcce4fda6778f17189640e0fa9b1190f178dc0d335c9012ddf629")
# print(account.address)
# print(account.key)

async def async_send_data():
    w3 = Web3(Web3.AsyncHTTPProvider("https://goerli.infura.io/v3/bbd5ce33856f4a188df9a144746934e4"),
              modules={'eth': (AsyncEth,)}, middlewares=[])
    myContract = w3.eth.contract(address="0x675Cb077282d22eF8B25A02ed279B8fb50da7769", abi=ABI)
    w3.eth.default_account = '0x41c9288b78090946db0fd6d32D8cB1fEfe18134B'
    pk = "cdd47b2a4f9bcce4fda6778f17189640e0fa9b1190f178dc0d335c9012ddf629"
    print(w3.eth.default_account)
    uuid = uuid4()
    url = Web3.toHex(b'url tester')
    git = Web3.toHex(b'git_tester')
    eml = Web3.toHex(b'email tester')
    hsh = myContract.functions.mint(
        w3.toChecksumAddress('0x9a56A3492d13E26E9C56B4Be3E30918e5F551684'), 12,
        [url, git, eml]).build_transaction({'nonce': w3.eth.get_transaction_count(w3.eth.default_account)})
    # shsh = w3.eth.account.signTransaction(hsh, pk)
    # tx = w3.eth.send_raw_transaction(shsh.rawTransaction)
    coinbase = await w3.eth.coinbase
    print(coinbase)
    return '1'


async def create():
    return await asyncio.get_event_loop().run_in_executor(None, hashpw, '1'.encode(), gensalt())


# a = asyncio.run(create())
# a = hashpw('1'.encode(), gensalt())
# # print(a)
# # asyncio.run(async_send_data())
# # print(Web3.toHex(a))
# # s = time.time()
# # for i in range(10):
# b = Web3.solidityKeccak(['bytes32'], ['0x' + '1'.encode().hex()]).hex()
# print(type(b))
# a = hashpw(str(i).encode(), gensalt())
# print(b.hex())
# print(time.time() - s)
