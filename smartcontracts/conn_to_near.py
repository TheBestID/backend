from asyncio import get_event_loop
from uuid import UUID, uuid4

import near_api
from web3 import Web3


def test():
    contract_id = "sbt.soul_dev.testnet"
    signer_id = "sbt.soul_dev.testnet"
    signer_key = 'ed25519:zXH65UModcNadRDPv7zVKv76tX3u2oZdeY5t2iMyp2Dz73p8ZLdsQPWwm1G7ZD5McFJkMwr9MGJcjLycKBJFJrP'
    args = {'new_id': 123, }

    near_provider = near_api.providers.JsonProvider("https://rpc.testnet.near.org")
    key_pair = near_api.signer.KeyPair(signer_key)
    signer = near_api.signer.Signer(signer_id, key_pair)
    account1 = near_api.account.Account(near_provider, signer, signer_id)
    # print(account.state)
    # account.access_key['nonce'] = 105106077000002

    out = account1.function_call(contract_id, "mint", [111, 'souldev.testnet'])

    # print(account.view_function(contract_id, "ping_string", []))
    print(out)


async def near_mint(contract, account, address: str):
    return await get_event_loop().run_in_executor(None, __near_mint, contract, account, address)


def __near_mint(contract, account, address: str):
    uuid = uuid4()
    account.function_call(contract, "mint", [uuid.int, address])
    return uuid


async def near_claim(contract, hash_email, github_token):
    return {'contractId': contract,
            'method': 'claim',
            'args': [hash_email, github_token],
            'gas': 1e14,
            'deposit': 0}
