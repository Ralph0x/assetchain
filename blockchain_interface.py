from web3 import Web3
from web3.middleware import geth_poa_middleware
import os
from dotenv import load_dotenv

load_dotenv()

WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI")
web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))

web3.middleware_onion.inject(geth_poa_middleware, layer=0)

ACCOUNT_PRIVATE_KEY = os.getenv("ACCOUNT_PRIVATE_KEY")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")

web3.eth.default_account = ACCOUNT_ADDRESS

def deploy_contract(compiled_contract):
    Contract = web3.eth.contract(abi=compiled_contract['abi'], bytecode=compiled_contract['bin'])
    tx_hash = Contract.constructor().transact({'from': ACCOUNT_ADDRESS, 'gas': 4000000})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.contractAddress

def interact_with_contract(contract_address, contract_abi, function_name, *args):
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    txn = contract.functions[function_name](*args).buildTransaction({
        'from': ACCOUNT_ADDRESS,
        'nonce': web3.eth.getTransactionCount(ACCOUNT_ADDRESS),
        'gas': 4000000
    })
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=ACCOUNT_PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

def tokenize_asset(contract_address, contract_abi, asset_details):
    tx_receipt = interact_with_contract(contract_address, contract_abi, 'tokenizeAsset', asset_details)
    return tx_receipt

def confirm_transaction(tx_hash):
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.status