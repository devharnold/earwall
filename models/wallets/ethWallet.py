from eth_account import Account
import os
from web3 import Web3
from cryptography.fernet import Fernet

# generate a private key
private_key = os.urandom(32)
private_key_hex = private_key.hex()

# generate the account from the private key
account = Account.from_key(private_key_hex)

# print wallet details
print(f"Private key: {account.private_key.hex()}")
print(f"Public key: {account._key_obj.public_key}")
print(f"Ethereum address: {account.address}")



key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt the private key
cipher_text = cipher_suite.encrypt(account.private_key)
print(f"Encrypt Private Key: {cipher_text}")



# connecting to a web3 provider
w3 = Web3(Web3.HTTPProvider(''))

# Setup the transaction
tx = {
    'to': '',
    'value': ''
    'gas': 2000000,
    'gasPrice': w3.toWei('50', 'gwei'),
    'nonce': w3.eth.get_transaction_count(account.address),
    'chainId': # service provider chain id
}

# Sign the transaction with the private key
signed_tx = w3.eth.account.sign_transaction(tx, account.privateKey)

# Send the transaction
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

print(f'Transaction hash: {w3.toHex(tx_hash)}')