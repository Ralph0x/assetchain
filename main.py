from flask import Flask, request, jsonify
from web3 import Web3
import json

app = Flask(__name__)

WEB3_PROVIDER = 'http://localhost:8545'
CONTRACT_ADDRESS = '0xYourContractAddress'
CONTRACT_ABI = '[]'

web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))
abi = json.loads(CONTRACT_ABI)

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

@app.route('/tokenize_asset', methods=['POST'])
def tokenize_asset():
    request_json = request.get_json(silent=True)  
    if not request_json or 'owner_address' not in request_json or 'asset_details' not in request_json:
        return jsonify({'error': 'Bad request'}), 400

    owner_address = request_json['owner_address']
    asset_details = request_json['asset_details']
    nonce = web3.eth.getTransactionCount(owner_address)

    txn_dict = contract.functions.tokenizeAsset(asset_details).buildTransaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
    })

    return jsonify({'message': 'Asset tokenization transaction sent'}), 200

@app.route('/verify_ownership', methods=['GET'])
def verify_ownership():
    owner_address = request.args.get('owner_address')
    token_id = request.args.get('token_id')

    if not owner_address or not token_id:
        return jsonify({'error': 'Bad request'}), 400

    is_owner = contract.functions.verifyOwnership(owner_address, int(token_id)).call()

    return jsonify({'is_owner': is_owner}), 200

@app.route('/transfer_asset', methods=['POST'])
def transfer_asset():
    request_json = request.get_json(silent=True)  
    if not request_json or 'from_address' not in request_json or 'to_address' not in request_json or 'token_id' not in request_json:
        return jsonify({'error': 'Bad request'}), 400

    from_address = request_json['from_address']
    to_address = request_json['to_address']
    token_id = request_json['token_id']
    nonce = web3.eth.getTransactionCount(from_address)

    txn_dict = contract.functions.transferAsset(to_address, int(token_id)).buildTransaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
    })

    return jsonify({'message': 'Asset transfer transaction sent'}), 200

@app.route('/get_asset_details', methods=['GET'])
def get_asset_details():
    token_id = request.args.get('token_id')
    
    if not token_id:
        return jsonify({'error': 'Bad request'}), 400
    
    asset_details = contract.functions.getAssetDetails(int(token_id)).call()
    
    return jsonify({'asset_details': asset_details}), 200

if __name__ == '__main__':
    app.run(debug=True)