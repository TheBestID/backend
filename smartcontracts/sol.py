from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import transfer_checked, TransferCheckedParams

from solana.rpc.commitment import Confirmed 
from solana.rpc.async_api import AsyncClient
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solana.keypair import Keypair
#import solana
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.system_program import TransferParams, transfer
from solana.transaction import Transaction, TransactionInstruction

import asyncio

async def main():
    secret_key = [125,123,66,130,150,91,98,26,47,197,131,62,91,244,99,113,85,167,103,195,244,36,142,107,203,77,179,13,28,130,7,200,239,176,224,96,126,147,134,207,124,45,183,30,73,76,195,72,112,203,92,121,52,175,23,42,243,156,116,143,162,183,244,225]
    keyipair = Keypair.from_secret_key(bytes(secret_key))
    async with AsyncClient("https://api.devnet.solana.com") as client:
        res = await client.is_connected()
        #Transaction(fee_payer=Keypair.public_key, instructions=TransactionInstruction(keys=Keypair, program_id='EaSgH9WzMJJVdBC2xKmiJMEr8MXHVZaLxHyMS5JmUZat')).sign(keyipair)

#         #transaction = Transaction(fee_payer=keyipair.public_key).from_solders()
# #         transaction = Transaction()
# #         #program_id='EaSgH9WzMJJVdBC2xKmiJMEr8MXHVZaLxHyMS5JmUZat',
# #         owner = Keypair.from_secret_key(bytes('3QnMsP9JQjcVNM2oPd2KKhpfxCxNZPAixkso1sj3yx4NRz5H7rcERjCFAsde1jN3ZhTToQrJi2VCVxLQfod3eQPQ'.encode()))

# #         transaction.add(TransactionInstruction(owner, program_id='EaSgH9WzMJJVdBC2xKmiJMEr8MXHVZaLxHyMS5JmUZat'))
# #         #owner = Keypair() # <-- need the keypair for the token owner here! 5j22en4YDzDNzmGm7WWVxxYGDQ3Y873p7joVbKncZ1Ke
        
        
# #         signature = await sendTransaction(transaction, res);
        to = Keypair.from_secret_key(bytes('3QnMsP9JQjcVNM2oPd2KKhpfxCxNZPAixkso1sj3yx4NRz5H7rcERjCFAsde1jN3ZhTToQrJi2VCVxLQfod3eQPQ'.encode()))
# #         await res.confirmTransaction(signature, "processed");
# # )     
#         #print(to)
        txn = Transaction().add(transfer(TransferParams(from_pubkey=keyipair.public_key, to_pubkey=to.public_key, lamports=1000000)))
        (await client.send_transaction(txn, keyipair)).value
        #print(await client.get_account_info(keyipair.public_key, encoding='jsonParsed'))


async def test():
    secret_key = [125,123,66,130,150,91,98,26,47,197,131,62,91,244,99,113,85,167,103,195,244,36,142,107,203,77,179,13,28,130,7,200,239,176,224,96,126,147,134,207,124,45,183,30,73,76,195,72,112,203,92,121,52,175,23,42,243,156,116,143,162,183,244,225]
    keyipair = Keypair.from_secret_key(bytes(secret_key))
    async with AsyncClient("https://api.devnet.solana.com") as client:
        res = await client.is_connected()
        print(await client.get_program_accounts(PublicKey('EaSgH9WzMJJVdBC2xKmiJMEr8MXHVZaLxHyMS5JmUZat')))

asyncio.run(test())



