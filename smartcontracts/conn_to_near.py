import near_api
from web3 import Web3

contract_id = "sbt.soul_dev.testnet"
signer_id = "sbt.soul_dev.testnet"
signer_key = 'ed25519:3gmjx9r37mpY5kPbyG3WpsrpjNpcWPdDxdWpXPAaDYUsRpYmk19w93Fe8T7p2Rirw71hdaMPqQyjfimSpcX9QCaK'
args = {'new_id': 123, }

near_provider = near_api.providers.JsonProvider("https://rpc.testnet.near.org")
key_pair = near_api.signer.KeyPair(signer_key)
signer = near_api.signer.Signer(signer_id, key_pair)
account = near_api.account.Account(near_provider, signer, signer_id)
# print(account.state)
# account.access_key['nonce'] = 105106077000002

out = account.function_call(contract_id, "mint", [111, 'souldev.testnet'])

# print(account.view_function(contract_id, "ping_string", []))
print(out)
