from web3 import Web3
from web3.middleware import geth_poa_middleware
import os
from dotenv import load_dotenv

load_dotenv()

WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI")
try:
    web3_interface = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))
except Exception as e:
    print(f"Failed to connect to the provider: {e}")
    raise

try:
    web3_interface.middleware_onion.inject(geth_poa_middleware, layer=0)
except Exception as e:
    print(f"Failed to inject middleware: {e}")
    raise

ACCOUNT_PRIVATE_KEY = os.getenv("ACCOUNT_PRIVATE_KEY")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")

web3_interface.eth.default_account = ACCOUNT_ADDRESS

def deploy_smart_contract(compiled_smart_contract):
    try:
        Contract = web3_interface.eth.contract(abi=compiled_smart_contract['abi'], bytecode=compiled_smart_contract['bin'])
        transaction_hash = Contract.constructor().transact({'from': ACCOUNT_ADDRESS, 'gas': 4000000})
        transaction_receipt = web3_interface.eth.wait_for_transaction_receipt(transaction_hash)
    except Exception as e:
        print(f"Failed to deploy contract: {e}")
        raise
    return transaction_receipt.contractAddress

def call_contract_function(contract_address, contract_abi, function_name, *function_arguments):
    try:
        contract_instance = web3_interface.eth.contract(address=contract_address, abi=contract_abi)
        transaction_details = contract_instance.functions[function_name](*function_arguments).buildTransaction({
            'from': ACCOUNT_ADDRESS,
            'nonce': web3_interface.eth.getTransactionCount(ACCOUNT_ADDRESS),
            'gas': 4000000
        })
        signed_transaction = web3_interface.eth.account.sign_transaction(transaction_details, private_key=ACCOUNT_PRIVATE_KEY)
        transaction_hash = web3_interface.eth.send_raw_transaction(signed_transaction.rawTransaction)
        transaction_receipt = web3_interface.eth.wait_for_transaction_receipt(transaction_hash)
    except Exception as e:
        print(f"Failed to call contract function {function_name}: {e}")
        raise
    return transaction_receipt

def tokenize_asset_on_chain(contract_address, contract_abi, asset_details):
    try:
        transaction_receipt = call_contract_function(contract_address, contract_abi, 'tokenizeAsset', asset_details)
    except Exception as e:
        print(f"Failed to tokenize asset on chain: {e}")
        raise
    return transaction_receipt

def query_contract_function(contract_address, contract_abi, function_name, *function_arguments):
    try:
        contract_instance = web3_interface.eth.contract(address=contract_address, abi=contract_abi)
        result = contract_instance.functions[function_name](*function_arguments).call()
    except Exception as e:
        print(f"Failed to query contract function {function_name}: {e}")
        raise
    return result

def verify_transaction(transaction_hash):
    try:
        transaction_receipt = web3_interface.eth.wait_for_transaction_receipt(transaction_hash)
    except Exception as e:
        print(f"Failed to verify transaction: {e}")
        raise
    return transaction_receipt.status