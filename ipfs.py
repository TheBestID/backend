# import ipfshttpclient

# client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')

# print(client)

# import requests, json
# import cid



# req_id = 'Z2lkOi8vZmlsZWJhc2UvQXNzZXQvMTA4MzQ1Njc4Mw'
# req_id = 'Z2lkOi8vZmlsZWJhc2UvQXNzZXQvMTA4MzYyNzI2Mg'
# token = 'NTREQjZEMjRDRUVGNzUwM0RDRjY6T1dpczFyRFlIcDZnZmEwVWFEWVlac0ZTNUlzNXF3aWFoR2Iwd1NrSTpzb3VsZGV2'


header = {'Authorization': 'Bearer NTREQjZEMjRDRUVGNzUwM0RDRjY6T1dpczFyRFlIcDZnZmEwVWFEWVlac0ZTNUlzNXF3aWFoR2Iwd1NrSTpzb3VsZGV2'}
# cid = 'Z2lkOi8vZmlsZWJhc2UvQXNzZXQvMTA4MzYyNzI2Mg'
# cid = 'Z2kJK2JNKJDSNjknjfnskJFNkjfndj3rjn32ejdnsk'

# cid = 'bafybeihbfkn5afsjep2jd65gn5vedh7vpvp6i6avfu5za7fnnhsvfutzjk'

# r = requests.post('https://s3.filebase.com', headers=header, json={
#     'cid': 'bafybeihbfkn5afsjep2jd65gn5vedh7vpvp6i6avfu5za7fnnadvfutzjk', 
#     'name': 'file',
#     'meata': {
#         'key_name': 'myname'
#     }
# })

# a = cid.toString('base-16')

# print(a)


# r = requests.post('https://api.filebase.io/v1/ipfs/pins', headers=header, json={
#      'name' : 'soul 2',
#      'cid' : 'bafybeihbfkn5afsjep2jd65gn5veas7vpvp6i6avfu5za7fnnhsvfutzjk', 
#      'meta' : {'key_name': "value"},
#      'SecretKey': token

#  })

#r = requests.get('https://api.filebase.io/v1/ipfs/pins', headers=header, json={'requestid': req_id})

# print(r)
#print(r.json()['results'])


# import boto3
# import requests
# import json

# from botocore.config import Config

# s3 = boto3.client('s3')

# boto_config = Config(
# 					region_name = 'us-east-1',
# 					signature_version = 's3v4')

# s3 = boto3.client(
# 					's3',
# 					endpoint_url = 'https://s3.filebase.com',
# 					aws_access_key_id='54DB6D24CEEF7503DCF6',
# 					aws_secret_access_key='OWis1rDYHp6gfa0UaDYYZsFS5Is5qwiahGb0wSkI',
# 					config=boto_config)

# bucket = 'souldev'
# key= 'text'

# response = s3.generate_presigned_url('put_object', Params={'Bucket':bucket,'Key':key}, ExpiresIn=3600, HttpMethod='PUT')

# print (response)

# if response is None:
# 		exit(1)

# response = requests.put(response)

# print('PUT status_code: ', response.status_code)
# print('PUT content: ', response.content)


from aleph_client.asynchronous import get_posts, create_store, storage_push_file
from aleph_client.chains.ethereum import ETHAccount
from fastapi import FastAPI
import asyncio
import json, requests

tk = 'QmVf6rKJvdFSReA9F5dCNjytvqDhNSQF89K1K1PZwRp5Zi'

async def get_hash():
    pr_key = 'c196b987045f400286f555384910f253108cb94b6f832e5a0ff7df01a7abadba'

    acc = ETHAccount(pr_key)

    #image = open("mavrodi.jpg", "rb").read()

    file = json.dumps({'meta_data': 'my info',
            })

    hash = await create_store(file_content=bytes(file, 'utf-8') , account=acc, storage_engine="ipfs")
    #await get_posts()
    #hash = await storage_push_file(file_content=file)
    print(hash)

def try_file_base():
    r = requests.post('https://s3.filebase.com', headers=header, json={
    'cid': 'bafybeihbfkn5afsjep2jd65gn5vedh7vpvp6i6avfu5za7fnnadvfutzjk', 
    'name': 'file',
    'meta': {
    'key_name': 'myname'
     }
 }) 
    print(r.content)


def try_read_base():
    r = requests.get('https://api.filebase.io/v1/ipfs/pins', headers=header, json={'requestid': req_id})


def pin_obj():
    r = requests.post('https://api.filebase.io/v1/ipfs/pins', headers=header, json={'cid': tk, 'name':'First name'})
    print(r.content)


from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from smartcontracts.abi import achivement_ABI
from smartcontracts.contracts_id import achivement_id


def check_sk(address):
    url = 'https://goerli.infura.io/v3/bbd5ce33856f4a188df9a144746934e4'
    web3 = Web3(Web3.HTTPProvider(url))
    print(web3.isConnected())
    contract = web3.eth.contract(address=achivement_id  , abi=achivement_ABI)
    key = contract.functions.mint([5, '0x41c9288b78090946db0fd6d32D8cB1fEfe18134B', '0x41c9288b78090946db0fd6d32D8cB1fEfe18134B', False, 'first sbt']).buildTransaction({'nonce': web3.eth.get_transaction_count(address), 'from': address})

    signed_tx = web3.eth.account.signTransaction(key, private_key='cdd47b2a4f9bcce4fda6778f17189640e0fa9b1190f178dc0d335c9012ddf629')
    web3.eth.sendRawTransaction(signed_tx.rawTransaction)


def get_sbt(address):
    url = 'https://goerli.infura.io/v3/bbd5ce33856f4a188df9a144746934e4'
    web3 = Web3(Web3.HTTPProvider(url))
    print(web3.isConnected())

    contract = web3.eth.contract(address=achivement_id  , abi=achivement_ABI)
    return contract.functions.getAchievementInfo(5).call({'from': address})
    #key = contract.functions.getAchievementInfo(5).buildTransaction({'nonce': web3.eth.get_transaction_count(address), 'from': address})
    #signed_tx = web3.eth.account.signTransaction(key, private_key='cdd47b2a4f9bcce4fda6778f17189640e0fa9b1190f178dc0d335c9012ddf629')
    #tx = web3.eth.sendRawTransaction(signed_tx.rawTransaction)


#check_sk('0x41c9288b78090946db0fd6d32D8cB1fEfe18134B')
from smartcontracts.abi import ABI3

def test_smart():
    url = 'https://goerli.infura.io/v3/bbd5ce33856f4a188df9a144746934e4'
    web3 = Web3(Web3.HTTPProvider(url))
    print(web3.isConnected())

    contract = web3.eth.contract(address='0x328Bc12b497389f687DAaeDE8AbDd190dcE6cF54'  , abi=ABI3)
    contract.functions.burn(5).call({'from': address})


def test():
    url = 'https://goerli.infura.io/v3/bbd5ce33856f4a188df9a144746934e4'
    web3 = Web3(Web3.HTTPProvider(url))
    print(Web3)

    #key contract.functions.getAchievementInfo(5).call({'from': address})
#r = requests.get('https://ipfs.io/ipfs/QmZuFPz7Wz7F4ZndiuE9HmVMX4qorqZHUeisUAtzGyPJiF')


#print(json.loads(r.content).get('mata_data'))

    #print(hash._get_value())
# pr_key = 'c196b987045f400286f555384910f253108cb94b6f832e5a0ff7df01a7abadba'

# acc = ETHAccount(pr_key)

# file = open("mavrodi.jpg", "rb").read()

# hash = create_store(file_content=file, account=acc, storage_engine="ipfs")

#loop = asyncio.get_event_loop().run_until_complete(get_hash())
# loop.run_until_complete(get_hash())
# oop.close()

#asyncio.run(get_hash())
import near_api

def test_near():
        contract_id = "sbt.soul_dev.testnet"
        signer_id = "soul_dev.testnet.sbt"
        signer_key = "ed25519:3gmjx9r37mpY5kPbyG3WpsrpjNpcWPdDxdWpXPAaDYUsRpYmk19w93Fe8T7p2Rirw71hdaMPqQyjfimSpcX9QCaK"
        args = {"counter": 1, "action": "increase"}

        near_provider = near_api.providers.JsonProvider("https://rpc.testnet.near.org")
        key_pair = near_api.signer.KeyPair(signer_key)
        signer = near_api.signer.Signer(signer_id, key_pair)
        account = near_api.account.Account(near_provider, signer)
        near_api
        out = account.function_call(contract_id, "counter_set", args, )

        #print(out)

test_near