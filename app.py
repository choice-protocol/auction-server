#
# Required imports
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from time import time


#https://github.com/flashbots/web3-flashbots
#from eth_account.signers.local import LocalAccount
#from web3 import Web3, HTTPProvider
#from flashbots import flashbot
#from eth_account.account import Account
#import os
#ETH_ACCOUNT_SIGNATURE: LocalAccount = Account.from_key(os.environ.get("ETH_SIGNATURE_KEY"))
#w3 = Web3(HTTPProvider("http://localhost:8545"))
#flashbot(w3, ETH_ACCOUNT_SIGNATURE)


from dataclasses import asdict, dataclass
from pprint import pprint
from typing import Optional

import rlp
from eth_typing import HexStr
from eth_utils import keccak, to_bytes
from rlp.sedes import Binary, big_endian_int, binary
from web3 import Web3
from web3.auto import w3


class Transaction(rlp.Serializable):
    fields = [
        ("nonce", big_endian_int),
        ("gas_price", big_endian_int),
        ("gas", big_endian_int),
        ("to", Binary.fixed_length(20, allow_empty=True)),
        ("value", big_endian_int),
        ("data", binary),
        ("v", big_endian_int),
        ("r", big_endian_int),
        ("s", big_endian_int),
    ]


@dataclass
class DecodedTx:
    hash_tx: str
    from_: str
    to: Optional[str]
    nonce: int
    gas: int
    gas_price: int
    value: int
    data: str
    chain_id: int
    r: str
    s: str
    v: int


def hex_to_bytes(data: str) -> bytes:
    return to_bytes(hexstr=HexStr(data))


def decode_raw_tx(raw_tx: str):
    tx = rlp.decode(hex_to_bytes(raw_tx), Transaction)
    hash_tx = Web3.toHex(keccak(hex_to_bytes(raw_tx)))
    from_ = w3.eth.account.recover_transaction(raw_tx)
    to = w3.toChecksumAddress(tx.to) if tx.to else None
    data = w3.toHex(tx.data)
    r = hex(tx.r)
    s = hex(tx.s)
    chain_id = (tx.v - 35) // 2 if tx.v % 2 else (tx.v - 36) // 2
    return DecodedTx(hash_tx, from_, to, tx.nonce, tx.gas, tx.gas_price, tx.value, data, chain_id, r, s, tx.v)

raw_tx = "0xf8a910850684ee180082e48694a0b86991c6218b36c1d19d4a2e9eb0ce3606eb4880b844a9059cbb000000000000000000000000b8b59a7bc828e6074a4dd00fa422ee6b92703f9200000000000000000000000000000000000000000000000000000000010366401ba0e2a4093875682ac6a1da94cdcc0a783fe61a7273d98e1ebfe77ace9cab91a120a00f553e48f3496b7329a7c0008b3531dd29490c517ad28b0e6c1fba03b79a1dee" 








# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
default_app = initialize_app()
db = firestore.client()

bids_ref = db.collection('bids')
txs_ref = db.collection('txs')

@app.route('/bid', methods=['POST'])
def bid():
    """
        bid() : Add bid to Firestore with bids extracted from their bodies
    """
    try:
        id = hash(request.json['bundle'])
        # the users transaction in the request bundle needs to be checked for the bid value that and added to the saved json
        bids_ref.document(id).set(request.json)
        
        bid_value
        
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/close', methods=['GET'])
def close():
    """
        dispatch any auction beyond their closing time that havent been dispatched yet (so hit this often).
    """
    for tx in db.collection(u'txs').where(u'timestamp', u'<', time() -6 ).where(u'Auction',u'==',u'open').stream():
        highest_bid,highest_bundle = 0,[]
        # dispatch to flashbots the winning bundle with user signature back in
        # 
        tx.update({"Auction": "closed", "Winner_Bundle": highest_bundle, Winner_bid:highest_bid})
 
@app.route('/list', methods=['GET'])
def list():
    #    db.collection(u'bids').where(u'time', u'>', request.json['tx'] ).stream()
    try:
        # Check if ID was passed to URL query
        tx_id = request.args.get('tx_id')
        if tx:
            tx = txs_ref.document(tx_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_open = [tx.to_dict() for tx in txs_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
    
    
