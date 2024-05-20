from flask import Flask, request, jsonify
from web3 import Web3
import os
import json

app = Flask(__name__)

web3_provider = os.getenv('WEB3_PROVIDER')
web3 = Web3(Web3.HTTPProvider(web3_provider))

contract_address = os.getenv('CONTRACT_ADDRESS')
abi = json.loads(os.getenv('CONTRACT_ABI'))

contract = web3.eth.contract(address=contract_address, abi=abi)

@app.route('/tokenize_asset', methods=['POST'])
def tokenize_asset():
    if not request.json or 'owner_address' not in request.json or 'asset_details' not in request.json:
        return jsonify({'error': 'Bad request'}), 400

    owner_address = request.json['owner_address']
    asset_details = request.json['asset_details']

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
    if not request.json or 'from_address' not in request.json or 'to_address' not in request.json or 'token_id' not in request.json:
        return jsonify({'error': 'Bad request'}), 400

    from_address = request.json['from_address']
    to_address = request.json['to_address']
    token_id = request.json['token_id']

    nonce = web3.eth.getTransactionCount(from_address)
    
    txn_dict = contract.functions.transferAsset(to_address, int(token_id)).buildTransaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
    })

    return jsonify({'message': 'Asset transfer transaction sent'}), 200

os.environ['WEB3_PROVIDER'] = 'http://localhost:8545'
os.environ['CONTRACT_ADDRESS'] = '0xYourContractAddress'
os.environ['CONTRACT_ABI'] = '[]'

if __name__ == '__main__':
    app.run(debug=True)