from flask import Flask, request, jsonify
from web3 import Web3
import json

app = Flask(__name__)

WEB3_PROVIDER_URI = 'http://localhost:8545'
SMART_CONTRACT_ADDRESS = '0xYourContractAddress'
CONTRACT_ABI_JSON = '[]'

web3_interface = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))
contract_abi = json.loads(CONTRACT_ABI_JSON)

asset_contract = web3_interface.eth.contract(address=SMART_CONTRACT_ADDRESS, abi=contract_abi)

@app.route('/tokenize_asset', methods=['POST'])
def tokenize_asset():
    req_data = request.get_json(silent=True)  
    if not req_data or 'owner_address' not in req_data or 'asset_details' not in req_data:
        return jsonify({'error': 'Bad request'}), 400

    asset_owner_address = req_data['owner_address']
    details_of_asset = req_data['asset_details']
    transaction_nonce = web3_interface.eth.getTransactionCount(asset_owner_address)

    transaction_parameters = asset_contract.functions.tokenizeAsset(details_of_asset).buildTransaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': web3_interface.toWei('50', 'gwei'),
        'nonce': transaction_nonce,
    })

    return jsonify({'message': 'Tokenization transaction pending'}), 200

@app.route('/verify_ownership', methods=['GET'])
def verify_asset_ownership():
    owner_address_query = request.args.get('owner_address')
    queried_token_id = request.args.get('token_id')

    if not owner_address_query or not queried_token_id:
        return jsonify({'error': 'Bad request'}), 400

    ownership_status = asset_contract.functions.verifyOwnership(owner_address_query, int(queried_token_id)).call()

    return jsonify({'is_owner': ownership_status}), 200

@app.route('/transfer_asset', methods=['POST'])
def transfer_asset():
    req_data = request.get_json(silent=True)  
    if not req_data or 'from_address' not in req_data or 'to_address' not in req_data or 'token_id' not in req_data:
        return jsonify({'error': 'Bad request'}), 400

    sender_address = req_data['from_address']
    recipient_address = req_data['to_address']
    asset_token_id = req_data['token_id']
    sender_nonce = web3_interface.eth.getTransactionCount(sender_address)

    transaction_parameters = asset_contract.functions.transferAsset(recipient_address, int(asset_token_id)).buildTransaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': web3_interface.toWei('50', 'gwei'),
        'nonce': sender_nonce,
    })

    return jsonify({'message': 'Transfer transaction pending'}), 200

@app.route('/get_asset_details', methods=['GET'])
def fetch_asset_details():
    asset_token_id_query = request.args.get('token_id')
    
    if not asset_token_id_query:
        return jsonify({'error': 'Bad request'}), 400
    
    details_of_asset = asset_contract.functions.getAssetDetails(int(asset_token_id_query)).call()
    
    return jsonify({'asset_details': details_of_asset}), 200

if __name__ == '__main__':
    app.run(debug=True)