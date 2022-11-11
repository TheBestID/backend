from asyncio import get_event_loop
import asyncio

from bcrypt import hashpw, gensalt
from web3 import Web3


from aleph_client.asynchronous import get_posts, create_store, create_post
from aleph_client.chains.ethereum import ETHAccount
from fastapi import FastAPI
import asyncio
import json, requests


async def hashing(data: str) -> str:
    return Web3.solidityKeccak(['bytes32'], [
        '0x' + (await get_event_loop().run_in_executor(None, hashpw, data.encode(), gensalt())).hex()]).hex()


async def git_token(githubCode: str):
    return '1'


def create_dump(username:str, description: str, isImage: bool, attributes=[], image=''):
    if isImage:
        return json.dumps({
                    "description": description, 
                    #"external_url": "https://openseacreatures.io/3", 
                    "image": "https://ipfs.io/ipfs/" + image, 
                    "name": username,
                    "attributes": attributes
                    })

    else:
        return json.dumps({
                    "description": description,  
                    "name": username,
                    "attributes": attributes
                    })
                        

async def loadToIpfs(data):
    with open('key.txt', 'r') as file:
        key = file.read()
        acc = ETHAccount(key)
        hash = await create_store(file_content=bytes(data, 'utf-8') , account=acc, storage_engine="ipfs")
        print(hash.content.item_hash)
        return hash.content.item_hash


def getFromIpfs(cid):
    r = requests.get('https://ipfs.io/ipfs/'+cid)
    return json.loads(r.content)
    

if __name__ == "__main__":
    print('QmVf6rKJvdFSReA9F5dCNjytvqDhNSQF89K1K1PZwRp5Zi' == 'QmVf6rKJvdFSReA9F5dCNjytvqDhNSQF89K1K1PZwRp5Zi')

    data = create_dump('username', 'my description', False, attributes=[{'some info': 'my info'}])
    
    #loop = asyncio.get_event_loop().run_until_complete(updateData(json.dumps({'info':'some info'}), old_sid='QmYgtCom5GnUXCbeLwTKyxhxkZb3DZKRe6wBnzDFSU6ZnX'))
    #getFromIpfs('QmVf6rKJvdFSReA9F5dCNjytvqDhNSQF89K1K1PZwRp5Zi')
    
    #loop = asyncio.get_event_loop().run_until_complete(getPost(refs='QmVf6rKJvdFSReA9F5dCNjytvqDhNSQF89K1K1PZwRp5Zi'))
    
    #loop = asyncio.get_event_loop().run_until_complete(loadToIpfs(json.dumps({'some info': 'old info'})))
#     #loop = asyncio.get_event_loop().run_until_complete(get_from_ipfs(test))

#     loop = asyncio.get_event_loop().run_until_complete(load_to_ipfs(data))

#     #get_from_ipfs()