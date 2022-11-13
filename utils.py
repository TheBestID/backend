import json
from asyncio import get_event_loop
from email.message import EmailMessage
from uuid import UUID

import requests
from aiosmtplib import SMTP
from aleph_client.asynchronous import create_store
from aleph_client.chains.ethereum import ETHAccount
from bcrypt import hashpw, gensalt
from web3 import Web3

PK = "cdd47b2a4f9bcce4fda6778f17189640e0fa9b1190f178dc0d335c9012ddf629"


async def hashing(data: str) -> str:
    return Web3.solidityKeccak(['bytes32'], [
        '0x' + (await get_event_loop().run_in_executor(None, hashpw, data.encode(), gensalt())).hex()]).hex()


async def git_token(githubCode: str):
    return '1'


def create_dump(username: str, description: str, isImage: bool, attributes=[], image=''):
    if isImage:
        return json.dumps({
            "description": description,
            # "external_url": "https://openseacreatures.io/3",
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


async def loadToIpfs(data, key):
    # return 'IPFS relax but still work ^_^'
    acc = ETHAccount(key)
    hash = await create_store(file_content=bytes(data, 'utf-8'), account=acc, storage_engine="ipfs")
    print(hash.content.item_hash)
    return hash.content.item_hash


def getFromIpfs(cid):
    r = requests.get('https://ipfs.io/ipfs/' + cid)
    return json.loads(r.content)


async def send_email(email, hash_email, github_token, email_token: UUID, e_from, e_pass):
    message = EmailMessage()
    message["From"] = e_from
    message["To"] = email
    message["Subject"] = "Verification!"
    message.set_content(
        f"To pass verification, follow the link:\nhttp://localhost:3000/success-email?code={github_token}&email_token={email_token.hex}&email={hash_email}")
    try:
        async with SMTP(hostname="smtp.gmail.com", port=465, use_tls=True, username=e_from, password=e_pass) as smtp:
            await smtp.send_message(message)
        return True
    except:
        return False


# asyncio.get_event_loop().run_until_complete(
#     send_email('agibalov1294@gmail.com', 'hash_email111', 'github_token111', uuid.uuid4(), "souldev.web3@gmail.com",
#                "zzolvnzkmvkywerq"))


if __name__ == "__main__":
    print('QmVf6rKJvdFSReA9F5dCNjytvqDhNSQF89K1K1PZwRp5Zi' == 'QmVf6rKJvdFSReA9F5dCNjytvqDhNSQF89K1K1PZwRp5Zi')

    data = create_dump('username', 'my description', False, attributes=[{'some info': 'my info'}])
