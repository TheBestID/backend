from web3 import Web3
from smartcontracts.abi import ABI
import time


def send_data(smth: dict):
    pass
    return '1'


def get_data(smth):
    start = time.time()
    w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/bbd5ce33856f4a188df9a144746934e4"))
    # print(w3.isConnected())

    myContract = w3.eth.contract(address="0x61Cd0c3044F291A2A7fe08596D36Efd799cb7092", abi=ABI)
    print(myContract.functions.retrieve().call())
    print(time.time() - start)
    pass
    return {'Тестовые': "Данные"}
