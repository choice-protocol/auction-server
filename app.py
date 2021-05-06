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
block_bidders_ref = db.collection('block_bidders')


@app.route('/bid', methods=['POST'])
def create():
    """
        TODO:
        1) check the block has not been mined already (and thus the auction is closed)
        2) check the signature is valid before the set, to avoid permision troulbe
        One document per block per bidder
        e.g. json={'block': '12375272', 'bid': '0.00001', 'relay_http_adress':'infura_smarter.io','bidder_address':'0xgqeqin2152342312de1w1', signature:'1x34qz q24tq32xtq34ztx34t34' }
    """
    try:
        id = str(hash( request.json['block']  +  request.json['bidder_address'] ) )+ request.json['block'] + '-' +  request.json['bidder_address']
        # the hash is there to avoid hotspots 
        block_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/winner', methods=['GET'])
def read():
    """
        read() : who won if the block is mined, no peeking otherwise (blind auctions)
    """
    # Note: Use of CollectionRef stream() is prefered to get()
    bids = db.collection('block_bidders').where(u'block', u'==', True).stream()

    max_bid = {'bid':0}
    for bid in bids:
        if bid['bid'] >     max_bid['bid']:
        max_bid = bid
    return max_bid
    
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
