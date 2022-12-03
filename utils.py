import json
from asyncio import get_event_loop
from email.message import EmailMessage
from uuid import UUID, uuid4

import aioboto3
import requests
from aiosmtplib import SMTP
from aleph_client.asynchronous import create_store
from aleph_client.chains.ethereum import ETHAccount
from bcrypt import hashpw, gensalt
from sanic.request import File
from web3 import Web3
import urllib.request
import re

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
    acc = ETHAccount(key)
    hash = await create_store(file_content=bytes(data, 'utf-8'), account=acc, storage_engine="ipfs")
    return hash.content.item_hash


async def loadFile(data: File):
    filename = uuid4().hex + '.' + data.name.split('.')[-1]
    s = aioboto3.Session()
    async with s.client(service_name='s3',
                        aws_access_key_id='YCAJEDXwS0WgZ5GQ0iY2Oo5tb',
                        aws_secret_access_key='YCOBVG4vwwg0sFAQORe779ncGgsVJhijmQ5iupcm',
                        endpoint_url='https://storage.yandexcloud.net') as s3:
        await s3.put_object(Bucket='imagesdata', Key=filename, Body=data.body)
    return f'imagesdata/{filename}'


def getFromIpfs(cid):
    r = requests.get('https://ipfs.io/ipfs/' + cid)
    print(r.content)
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
    except Exception as e:
        return False


async def check_email(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return re.fullmatch(regex, email)


def check_link(link: str):
    resp = urllib.request.urlopen(link).getcode()
    if resp == 200:
        return True
    else:
        return False



async def compare_link(link: str, email: str):
    if email.find("@") > 0 and email.find(".") > 0:
        domain = email[email.find("@") + 1 : email.find(".")]
        print(domain)
    else:
        return False

    return (domain.lower() in link.lower())







# asyncio.get_event_loop().run_until_complete(
#     send_email('agibalov1294@gmail.com', 'hash_email111', 'github_token111', uuid.uuid4(), "souldev.web3@gmail.com",
#                "zzolvnzkmvkywerq"))


if __name__ == "__main__":
    #print('QmVf6rKJvdFSReA9F5dCNjytvqDhNSQF89K1K1PZwRp5Zi' == 'QmVf6rKJvdFSReA9F5dCNjytvqDhNSQF89K1K1PZwRp5Zi')

    #data = create_dump('username', 'my description', False, attributes=[{'some info': 'my info'}])

    print(check_link('https://ya.ru/?ysclid=lb7v2glqp1803676652'))