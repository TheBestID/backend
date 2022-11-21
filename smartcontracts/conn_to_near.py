import near_api
from web3 import Web3

contract_id = "sbt.soul_dev.testnet"
signer_id = "soul_dev.testnet"
signer_key = "ed25519:3gmjx9r37mpY5kPbyG3WpsrpjNpcWPdDxdWpXPAaDYUsRpYmk19w93Fe8T7p2Rirw71hdaMPqQyjfimSpcX9QCaK"
args = {"counter": 1, "action": "increase"}

near_provider = near_api.providers.JsonProvider("https://rpc.testnet.near.org")
key_pair = near_api.signer.KeyPair(signer_key)
signer = near_api.signer.Signer(signer_id, key_pair)
account = near_api.account.Account(near_provider, signer, signer_id)
print(near_api.account.Account.access_key.setter(('nonce', 1)))

out = account.function_call(contract_id, "get_num", args)

# print(out)
