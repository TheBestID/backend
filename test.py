from web3 import Web3
from smartcontracts.abi import ABI, ABI2 
#url = 'https://mainnet.infura.io/v3/bbd5ce33856f4a188df9a144746934e4'

url = 'https://goerli.infura.io/v3/bbd5ce33856f4a188df9a144746934e4'

mySoul = '0xfAaD7C92A849a216840603244A292AF42d0bd953'

nemySoul ='"0x61Cd0c3044F291A2A7fe08596D36Efd799cb7092"'

web3 = Web3(Web3.HTTPProvider(url))

serega = '0x41c9288b78090946db0fd6d32D8cB1fEfe18134B'

site_user = '0x9a56A3492d13E26E9C56B4Be3E30918e5F551684'

pr_key = 'c196b987045f400286f555384910f253108cb94b6f832e5a0ff7df01a7abadba'

pr_key_serg = 'cdd47b2a4f9bcce4fda6778f17189640e0fa9b1190f178dc0d335c9012ddf629'
#web3.eth.defaultAccount =  '0x5Efa2C1F12BF105afb83d2e3a18C1d2AcE91e598'
#web3.eth.defaultAccount =  web3.eth.accounts[0]
print(web3.isConnected())

#print(web3.fromWei(web3.eth.getBalance("0x5Efa2C1F12BF105afb83d2e3a18C1d2AcE91e598"), 'ether'))


test_soul = "0x1754a769B3A790239333f28B1d0cd3eb72485020"


contract = web3.eth.contract(address=test_soul  , abi=ABI2)

#print(contract.functions.retrieve().call())

#tx_hash = contract.functions.store(10).transact({'from' : serega})

#web3.eth.waitForTransactionReceipt(tx_hash)
#print(contract.functions.getID().call())

#key = contract.functions.Mint().buildTransaction({'nonce': web3.eth.get_transaction_count(serega)})

hui = False

if hui:
    key = contract.functions.claimSBT(100).buildTransaction({'nonce': web3.eth.get_transaction_count(site_user)})

    signed_tx = web3.eth.account.signTransaction(key, private_key=pr_key)
    web3.eth.sendRawTransaction(signed_tx.rawTransaction)

#key = contract.functions.mint(1).buildTransaction({'nonce': web3.eth.get_transaction_count(serega)})
#signed_tx = web3.eth.account.signTransaction(key, private_key=pr_key_serg)
#web3.eth.sendRawTransaction(signed_tx.rawTransaction)

print(contract.functions.ping(11).call())

#print(signed_tx)



#key = contract.functions.claimSBT(10).buildTransaction({'nonce': web3.eth.get_transaction_count(serega)})

#print(key)
#signed_tx = web3.eth.account.signTransaction(key, private_key='cdd47b2a4f9bcce4fda6778f17189640e0fa9b1190f178dc0d335c9012ddf629')

#web3.eth.sendRawTransaction(signed_tx.rawTransaction)