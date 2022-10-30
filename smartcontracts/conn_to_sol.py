from web3 import Web3
from smartcontracts.abi import ABI
import time


async def send_data(smth: dict):
    w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/bbd5ce33856f4a188df9a144746934e4"))
    myContract = w3.eth.contract(address="0x61Cd0c3044F291A2A7fe08596D36Efd799cb7092", abi=ABI)
    a = myContract.functions.store(12).transact()
    print(a)
    return '1'


async def get_data(smth):
    w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/bbd5ce33856f4a188df9a144746934e4"))
    myContract = w3.eth.contract(address="0x61Cd0c3044F291A2A7fe08596D36Efd799cb7092", abi=ABI)
    a = myContract.functions.retrieve()
    return {'num': a}

# send_data(1)
