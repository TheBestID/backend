# import time
#
# import requests as requests
#
# start = time.time()
# r = requests.post('http://localhost:8000/user/address',
#                   json={'address': '134'})
# print(r.text, time.time() - start)
import json
import sys
import asyncio

import aioipfs


async def get():
    client = aioipfs.AsyncIPFS(maddr='/ip4/127.0.0.1/tcp/5001')
    print(client.session)

    a = await client.add_json({'popa11': "boba22"})
    print(a)

    params = {
        'arg': a['Hash'],
        'compress': 0,
        'compression-level': str(-1),
        'archive': 1
    }

    async with client.core.driver.session.post(client.core.url('get'), params=params) as resp:
        chunk = await resp.content.read()
        print(chunk.decode('ascii'))
    # b = await client.get(c)
    # print(b)

    await client.close()


asyncio.run(get())


async def add_files(files: list):
    client = aioipfs.AsyncIPFS(maddr='/ip4/127.0.0.1/tcp/5001')

    async for added_file in client.add(*files, recursive=True):
        print('Imported file {0}, CID: {1}'.format(
            added_file['Name'], added_file['Hash']))

    await client.close()
