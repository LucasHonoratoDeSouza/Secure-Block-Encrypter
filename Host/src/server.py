from flask import Flask, request, jsonify
from src.blockchain import Blockchain
from cryptography.fernet import Fernet

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json.get('data')
    key = request.json.get('key')
    if data and key:
        if isinstance(data, str) and isinstance(key, str):
            block_hash = blockchain.add_data(data, key.encode())
            blockchain.save_to_file("blockchain_data.pkl")
            return jsonify({"block_hash": block_hash}), 200
    return jsonify({"error": "Invalid data or key"}), 400

@app.route('/get_data/<block_hash>', methods=['GET'])
def get_data(block_hash):
    key = request.args.get('key')
    if block_hash and key:
        block = blockchain.get_data_by_hash(block_hash)
        if block:
            try:
                decrypted_data = blockchain.decrypt_data(block.data, key.encode())
                return jsonify({"data": decrypted_data}), 200
            except:
                return jsonify({"error": "Failed to decrypt data"}), 400
    return jsonify({"error": "Block not found or key missing"}), 404
