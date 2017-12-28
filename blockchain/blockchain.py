import hashlib
import json
from db import Database
from time import time
from flask import Flask, jsonify, request
from urllib.parse import urlparse
import requests
import global_constants as gc
import binascii as ba

class Blockchain(object):
    def __init__(self):

        self.nodes = set()
        self.database = Database()
        self.chain = self.database.getChain()
        self.current_transactions = []

        # Create the genesis block
        self.new_block(proof=100, block_hash=1)

    def register_node(self, address):

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def new_block(self, proof, block_hash=None):

        block = {
            'index': len(self.chain) + 1,
            'hash': block_hash or self.hash(self.chain[-1]),
            'timestamp': time(),
            'merkle_root': self.merkle_root([t['hash'] for t in self.current_transactions]),
            'transactions_number': len(self.current_transactions),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_index': len(self.chain),
            'node_identifier': gc.NODE_IDENTIFIER,
        }

        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        print(self.chain)
        #self.database.saveChain(self.chain)

        return block

    def new_transaction(self, transaction):

        self.current_transactions.append({
            'sender': transaction['sender'],
            'recipient': transaction['recipient'],
            'amount': transaction['amount'],
            'hash': self.hash(transaction)
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(item):

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(item, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def hash2(a, b):

        a1 = ba.unhexlify(a)[::-1]
        b1 = ba.unhexlify(b)[::-1]
        h = hashlib.sha256(hashlib.sha256(a1 + b1).digest()).digest()
        return ba.hexlify(h[::-1]).decode()

    @staticmethod
    def merkle_root(hash_list):

        if len(hash_list) == 1:
            return hash_list[0]
        if len(hash_list) == 0:
            return ''

        new_hash_list = []

        for i in range(0, len(hash_list) - 1, 2):
            new_hash_list.append(Blockchain.hash2(hash_list[i], hash_list[i + 1]))

        if len(hash_list) % 2 == 1:  # odd, hash last item twice
            new_hash_list.append(Blockchain.hash2(hash_list[-1], hash_list[-1]))

        return Blockchain.merkle_root(new_hash_list)

    @staticmethod
    def valid_proof(last_proof, proof):

        guess = f'{last_proof * proof / (last_proof/(proof + 1))}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

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
            if not self.valid_proof(last_block['proof'], block['proof']):
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

'''
def merkle_root(hash_list):

    if len(hash_list) == 1:
       return hash_list[0]
    if len(hash_list) == 0:
       return ''

    new_hash_list = []

    for i in range(0, len(hash_list) - 1, 2):
       new_hash_list.append(Blockchain.hash2(hash_list[i], hash_list[i + 1]))

    if len(hash_list) % 2 == 1:  # odd, hash last item twice
       new_hash_list.append(Blockchain.hash2(hash_list[-1], hash_list[-1]))

    return merkle_root(new_hash_list)
'''





app = Flask(__name__)

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    new_transaction_object = {
        'sender': gc.GENERATED_BLOCK,
        'recipient': gc.MY_WALLET_IDENTIFIER,
        'amount': gc.BLOCK_REWARD,
    }

    blockchain.new_transaction(new_transaction_object)

    # Forge the new Block by adding it to the chain
    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'hash': block['hash'],
        'transactions': block['transactions'],
        'proof': block['proof'],
    }
    print("New block with index = " + block['index'].__str__() + " and number of transactions = " + len(block['transactions']).__str__() + " was created successfully.")
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
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


@app.route('/chain', methods=['GET'])
def full_chain():
    print(blockchain.chain)
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.config['JSON_SORT_KEYS'] = False
    app.run(host='127.0.0.1', port=5000)



