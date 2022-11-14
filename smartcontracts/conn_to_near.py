import near_api
from web3 import Web3

contract_id = "contract.testnet"
signer_id = "signer.testnet"
signer_key = "ed25519:SXDVLyDiLUgnxxujbZdS9reypb9TaYG7LgTLA2Aq3yFoX1YNd76CEhF2D1yKmAcFGbFF46o5mvGHx5N7BqMUjzf"
args = {"counter": 1, "action": "increase"}

near_provider = near_api.providers.JsonProvider("https://rpc.testnet.near.org")
key_pair = near_api.signer.KeyPair(signer_key)
signer = near_api.signer.Signer(signer_id, key_pair)
account = near_api.account.Account(near_provider, signer, '1111')

out = account.function_call(contract_id, "counter_set", args)

print(out)
