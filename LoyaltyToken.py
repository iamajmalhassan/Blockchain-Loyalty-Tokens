from web3 import Web3
import json
import time
import sys
from eth_account import Account

#I am using Ganache; You can use your Infura link as url
url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(url))
account = input("Enter your account number : ")

# I am using hosted private keys, so I don't need to sign transactions. So, I am asking the user's private key to verify his account.
# This is not recommended, but I am excusing myself as it is just for demo purpose.
pvtKey = input("Enter your Private key : ")
acct = Account.from_key(pvtKey)
derived_account = acct.address
if derived_account!=account:
	print("Wrong private key!")
	print("Exiting...")
	time.sleep(2)
	sys.exit()
print(" ")
web3.eth.defaultAccount = web3.eth.accounts[0]
abi = json.loads('[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"redeemTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"transferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
address = web3.toChecksumAddress("0x69e70666D95724b918C29372957026Fb4B9FE9E1")
contract = web3.eth.contract(address=address,abi=abi)
while(1):
	print("What do you want to do?\n")
	print("1. Get Balance of Tokens.")
	print("2. Gift Tokens to another account.")
	print("3. Redeem your Tokens.")
	print("4. Mint Tokens (You need owner privileges).")
	print("5. Exit")
	c=int(input())
	if(c==1):
		# Get balance of tokens in your account.
		balance = contract.functions.balance(account).call()
		print("\nBalance is : ",balance)
		print(" ")
	if(c==2):
		# Gift/Transfer tokens to another account.
		amount = int(input("Enter the number of Tokens you want to Transfer : "))
		account2 = input("Enter the account you want to transfer the tokens to : ")
		print(" ")
		try:
			tx_hash = contract.functions.transferTokens(account2,amount).transact({'from':account})
			tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
			print("Transaction Successful.")
			print("Transaction Hash:  ",web3.toHex(tx_hash))
			print(" ")
		except:
			print("The Transaction did not go through. Try again...")
			time.sleep(2)

	if(c==3):
		# Redeem the tokens for gifts/discount - Transfers tokens back to the owner.
		amount = int(input("Enter the amount of Tokens :"))
		print(" ")
		try:
			tx_hash = contract.functions.redeemTokens(amount).transact({'from':account})
			tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
			print("Transaction Successful.")
			print("You can show your transaction hash to redeem your gift.")
			print("Transaction Hash:  ",web3.toHex(tx_hash))
			print(" ")
		except:
			print("The Transaction did not go through. Try again...")
			time.sleep(2)
	if(c==4):
		# Transfers the specified tokens into the owner's account. Only accessible by the owner.
		amount = int(input("Enter the amount : "))
		print(" ")
		try:
			tx_hash = contract.functions.mint(amount).transact({'from':account})
			tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
			print("Transaction Successful.")
			print("Transaction Hash: ",web3.toHex(tx_hash))
			print(" ")
		except:
			print("Only the owner can mint tokens.")
			time.sleep(2)
	if(c==5):
		print("\nExiting...")
		time.sleep(1)
		sys.exit()
