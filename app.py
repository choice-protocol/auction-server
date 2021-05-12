#
# Required imports
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from time import time
# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()

bids_ref = db.collection('bids')
bids_ref = db.collection('txs')

@app.route('/bid', methods=['POST'])
def bid():
    """
        bid() : Add bid to Firestore collection with request body.
    """
    try:
        id = hash(request.json['bundle'] + request.json['bidder'])
        bids_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/close', methods=['GET'])
def close():
    """
        dispatch any closed ones that havent been dispatched yet (so hit this often).
    """
    for tx in db.collection(u'tx').where(u'timestamp', u'<', time() -30 ).where(u'Auction',u'==',u'open').stream():
        highest_bid,highest_bundle = 0,[]
        for bids in db.collection(u'bids').where(u'tx',u'==',tx.tx ).stream():
               #calculate the value for the user of the bid
                bid_value = 0
                if bid_value > highest_bid:
                    highest_bid,highest_bundle=bid_value,bundle
        # Udpdate auction for the tx to closed:
        tx.update({"Auction": "closed", "Winner_Bundle": highest_bundle, Winner_bid:highest_bid})
 
@app.route('/list', methods=['GET'])
def list():
    #    db.collection(u'bids').where(u'time', u'>', request.json['tx'] ).stream()
    try:
        # Check if ID was passed to URL query
        tx = request.args.get('tx')
        if tx:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_open = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
    
    
