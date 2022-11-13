from uuid import uuid4, UUID

from eth_utils import to_checksum_address
from eth_utils import to_hex
from sanic import Blueprint
from sanic.response import Request, json

from database.achievements import add_achievements
from database.users import get_uuid, checkReg

achievements = Blueprint("achievements", url_prefix="/achievements")


@achievements.post("/add")
# @openapi.body({"application/json": VacancyAdd}, required=True)
async def add_achievement(request: Request):
    r = request.json
    w3 = request.app.config.get('web3')
    async with request.app.config.get('POOL').acquire() as conn:
        if not await checkReg(conn, r.get('address'), str(r.get('chainId'))):
            return json({'error': "Wallet isn't registered"}, 409)
        ach_uuid = uuid4()
        from_uuid = await get_uuid(conn, r.get('from_address'), r.get('chainId'))
        to_uuid = await get_uuid(conn, r.get('to_address'), r.get('chainId'))
        cid = await add_achievements(conn, ach_uuid, from_uuid, to_uuid)

        data = request.app.config.get('contract_ach').functions.mint(
            [ach_uuid.int, from_uuid.int, to_uuid.int, 1, False, cid]).build_transaction(
            {'nonce': w3.eth.get_transaction_count(to_checksum_address(r.get('from_address'))),
             'from': to_checksum_address(r.get('from_address'))
             })

        data['value'] = to_hex(data['value'])
        data['gas'] = to_hex(data['gas'])
        data['maxFeePerGas'] = to_hex(data['maxFeePerGas'])
        data['maxPriorityFeePerGas'] = to_hex(data['maxPriorityFeePerGas'])
        data['chainId'] = to_hex(data['chainId'])
        data['nonce'] = to_hex(data['nonce'])

        stx = w3.eth.account.signTransaction(data, request.app.config['account'].key)
        txHash = w3.eth.send_raw_transaction(stx.rawTransaction)
