from asyncio import get_event_loop
from uuid import UUID, uuid4

import near_api
from web3 import Web3


def test():
    my_key = "ed25519:2Y5S5mdivXGEBZ6WRLE6Bxvpjh57VVvrvdhXst3BqZRP29ZRkHV5wBPQWFpAYnfYTuFTFB8EKVEcn5MiF9csGtbG"
    my_id = "souldev.testnet"

    contr_key = 'ed25519:zXH65UModcNadRDPv7zVKv76tX3u2oZdeY5t2iMyp2Dz73p8ZLdsQPWwm1G7ZD5McFJkMwr9MGJcjLycKBJFJrP'
    contr_id = "sbt.soul_dev.testnet"
    args = {'new_id': 123, }

    near_provider = near_api.providers.JsonProvider("https://rpc.testnet.near.org")

    contr_key_pair = near_api.signer.KeyPair(contr_key)
    contr_signer = near_api.signer.Signer(contr_id, contr_key_pair)
    account_contr = near_api.account.Account(near_provider, contr_signer, contr_id)

    my_key_pair = near_api.signer.KeyPair(my_key)
    my_signer = near_api.signer.Signer(my_id, my_key_pair)
    account_my = near_api.account.Account(near_provider, my_signer, my_id)

    # print(account.state)
    # account.access_key['nonce'] = 105106077000002

    # out = account1.function_call(contract_id, "burn", ['souldev.testnet'])
    # print(out)

    out = account_my.function_call(contr_id, 'burn', [])
    print(out)

