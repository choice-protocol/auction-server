# app.py

# Required imports
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
block_ref = db.collection('blocks')

@app.route('/bid', methods=['POST'])
def create():
    """
        One collection per block, so id is the target block 
        e.g. json={'block': '12375272', 'bid': '0.00001', 'relay_http_adress':'infura_smarter.io','relay_eth_address':'0xgqeqin2152342312de1w1', signature:'1x34qz q24tq32xtq34ztx34t34' }
    """
    try:
        id = request.json['block']
        block_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/winner', methods=['GET'])
def read():
    """
        read() : lists all bids in a given block as JSON.
    """
    block_id = request.args.get('block')
    if block_id:
        block = block_ref.document(block_id).get()
        return jsonify(block.to_dict()), 200

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
