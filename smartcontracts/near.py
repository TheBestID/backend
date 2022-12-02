from asyncio import get_event_loop
from uuid import uuid4, UUID


async def mint(contract, account, address: str):
    return await get_event_loop().run_in_executor(None, __mint, contract, account, address)


def __mint(contract, account, address: str):
    uuid = uuid4()
    account.function_call(contract, "mint", [uuid.int, address])
    return uuid


async def claim(contract, hash_email, github_token):
    return {'contractId': contract,
            'method': 'claim',
            'args': [github_token, hash_email],
            'gas': 1e14,
            'deposit': 0}


async def burn(contract):
    return {'contractId': contract,
            'method': 'burn',
            'args': [],
            'gas': 1e14,
            'deposit': 0}


async def mint_achievement(contract, _type: int, from_uuid: UUID, to_uuid: UUID, verifier: UUID, cid: str,
                           balance: int):
    ach_uuid = uuid4()
    return ach_uuid, {'contractId': contract,
                      'method': 'mint',
                      'args': [ach_uuid.int, _type, from_uuid.int, to_uuid.int, False, verifier.int, False, cid,
                               balance],
                      'gas': 1e14,
                      'deposit': 0}
