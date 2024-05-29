from web3 import Web3
from web3.middleware import geth_poa_middleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Web3 provider
WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI")
web3_interface = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))

# Inject POA middleware compatibility
web3_interface.middleware_onion.inject(geth_poa_middleware, layer=0)

# Environment variables for account management
ACCOUNT_PRIVATE_KEY = os.getenv("ACCOUNT_PRIVATE_KEY")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")

# Set default account for transactions
web3_interface.eth.default_account = ACCOUNT_ADDRESS

def deploy_smart_contract(compiled_smart_contract):
    """
    Deploys a compiled smart contract to the blockchain.
    """
    Contract = web3_interface.eth.contract(abi=compiled_smart_contract['abi'], bytecode=compiled_smart_contract['bin'])
    transaction_hash = Contract.constructor().transact({'from': ACCOUNT_ADDRESS, 'gas': 4000000})
    transaction_receipt = web3_interface.eth.wait_for_transaction_receipt(transaction_hash)
    return transaction_receipt.contractAddress

def call_contract_function(contract_address, contract_abi, function_name, *function_arguments):
    """
    Interacts with a deployed contract by calling one of its functions.
    """
    contract_instance = web3_interface.eth.contract(address=contract_address, abi=contract_abi)
    transaction_details = contract_instance.functions[function_name](*function_arguments).buildTransaction({
        'from': ACCOUNT_ADDRESS,
        'nonce': web3_interface.eth.getTransactionCount(ACCOUNT_ADDRESS),
        'gas': 4000000
    })
    signed_transaction = web3_interface.eth.account.sign_transaction(transaction_details, private_key=ACCOUNT_PRIVATE_KEY)
    transaction_hash = web3_interface.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = web3_interface.eth.wait_for_transaction_receipt(transaction_hash)
    return transaction_receipt

def tokenize_asset_on_chain(contract_address, contract_abi, asset_details):
    """
    Tokenizes an asset by interacting with the smart contract.
    """
    transaction_receipt = call_contract_function(contract_address, contract_abi, 'tokenizeAsset', asset_details)
    return transaction_receipt

def verify_transaction(transaction_hash):
    """
    Confirms a transaction's success status.
    """
    transaction_receipt = web3_interface.eth.wait_for_transaction_receipt(transaction_hash)
    return transaction_receipt.status