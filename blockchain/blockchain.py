import crypto as cr
import requests
import strings as g
import db
from time import time
from flask import Flask, jsonify, request
from urllib.parse import urlparse


class Blockchain(object):

    def __init__(self):
        self.nodes = set()
        self.chain = db.get_blockchain()
        self.current_transactions = []

        # Create the genesis block
        self.new_block(proof=100, previous_hash=1)


    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)


    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'merkle_root': cr.merkle_root([t['hash'] for t in self.current_transactions]),
            'transactions_number': len(self.current_transactions),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_index': len(self.chain),
            'previous_hash': previous_hash or cr.block_hash(self.chain[-1]),
            'node_identifier': g.NODE_IDENTIFIER
        }

        block_hash_calc = {}
        for k in g.BLOCK_HASH_KEYS:
            block_hash_calc[k] = block[k]



        block['hash'] = cr.block_hash(block_hash_calc)

        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        print(g.NEW_BLOCK_CREATED_MSG + str(block['index']))
        db.save_blockchain(self.chain)

        return block


    def new_transaction(self, transaction):
        self.current_transactions.append({
            'sender': transaction['sender'],
            'recipient': transaction['recipient'],
            'amount': transaction['amount'],
            'hash': cr.block_hash(transaction)
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while cr.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof


    def valid_chain(self, chain):

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not cr.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True


    def resolve_conflicts(self):

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False


app = Flask(__name__)

blockchain = Blockchain()


@app.route(g.MINE_ROUTE, methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    new_transaction_object = {
        'sender': g.GENERATED_BLOCK,
        'recipient': g.MY_WALLET_IDENTIFIER,
        'amount': g.BLOCK_REWARD,
    }

    blockchain.new_transaction(new_transaction_object)

    # Forge the new Block by adding it to the chain
    block = blockchain.new_block(proof)

    response = {
        'message': g.NEW_BLOCK_FORGED_MSG,
        'index': block['index'],
        'hash': block['hash'],
        'transactions': block['transactions'],
        'proof': block['proof'],
    }

    return jsonify(response), 200


@app.route(g.NEW_TRANSACTION_ROUTE, methods=['POST'])
def new_transaction():
    values = request.get_json()
    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    # Create a new Transaction
    index = blockchain.new_transaction(values)
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route(g.FULL_CHAIN_ROUTE, methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route(g.NODE_REGISTER_ROUTE, methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return g.INVALID_NODES_LIST_ERR, 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': g.NEW_NODES_ADDED_MSG,
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route(g.RESOLVE_CONFLICTS_ROUTE, methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': g.CHAIN_REPLACED_MSG,
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': g.CHAIN_NOT_REPLACED_MSG,
            'chain': blockchain.chain
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.config['JSON_SORT_KEYS'] = False
    app.run(host='127.0.0.1', port=5000)



