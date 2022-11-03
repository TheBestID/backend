from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware  
from eth_account import Account
from eth_account.signers.local import LocalAccount
from smartcontracts.abi import ABI, ABI2 

url = 'https://goerli.infura.io/v3/bbd5ce33856f4a188df9a144746934e4'
user = '0x41c9288b78090946db0fd6d32D8cB1fEfe18134B'
private_key = 'cdd47b2a4f9bcce4fda6778f17189640e0fa9b1190f178dc0d335c9012ddf629'
contract_add = '0x7dbbc06936BD28db02cB9Df91373Cf35cF56c51f'



web3 = Web3(Web3.HTTPProvider(url))
print(web3.isConnected())


#login 
account: LocalAccount = Account.from_key(private_key)
web3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))



#test ping
contract = web3.eth.contract(address=contract_add  , abi=ABI2)

print(contract.functions.ping(11).call())


#print(contract.functions.ping(11).call())