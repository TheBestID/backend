from asyncio import get_event_loop
from uuid import uuid4

from eth_utils import to_checksum_address, to_hex


async def mint(provider, contract, account, address):
    return await get_event_loop().run_in_executor(None, __mint, provider, contract, account, address)


def __mint(provider, contract, account, address):
    uuid = uuid4()
    tx = contract.functions.mint(to_checksum_address(address), uuid.int).build_transaction(
        {'nonce': provider.eth.get_transaction_count(account.address)})
    stx = provider.eth.account.signTransaction(tx, account.key)
    txHash = provider.eth.send_raw_transaction(stx.rawTransaction)
    provider.eth.wait_for_transaction_receipt(txHash)
    return uuid


async def claim(provider, contract, address, hash_email, github_token):
    return await get_event_loop().run_in_executor(None, __claim, provider, contract, address, hash_email,
                                                  github_token)


def __claim(provider, contract, address, hash_email, github_token):
    data = contract.functions.claim([hash_email, github_token]).build_transaction(
        {'nonce': provider.eth.get_transaction_count(to_checksum_address(address)),
         'from': to_checksum_address(address)})

    data['value'] = to_hex(data['value'])
    data['gas'] = to_hex(data['gas'])
    data['maxFeePerGas'] = to_hex(data['maxFeePerGas'])
    data['maxPriorityFeePerGas'] = to_hex(data['maxPriorityFeePerGas'])
    data['chainId'] = to_hex(data['chainId'])
    data['nonce'] = to_hex(data['nonce'])

    return data


async def burn(provider, contract, address):
    return await get_event_loop().run_in_executor(None, __burn, provider, contract, address)


def __burn(provider, contract, address):
    data = contract.functions.burn().build_transaction(
        {'nonce': provider.eth.get_transaction_count(to_checksum_address(address)),
         'from': to_checksum_address(address)})

    data['value'] = to_hex(data['value'])
    data['gas'] = to_hex(data['gas'])
    data['maxFeePerGas'] = to_hex(data['maxFeePerGas'])
    data['maxPriorityFeePerGas'] = to_hex(data['maxPriorityFeePerGas'])
    data['chainId'] = to_hex(data['chainId'])
    data['nonce'] = to_hex(data['nonce'])

    return data
