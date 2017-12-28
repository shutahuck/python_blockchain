import json
import strings as g
import hashlib
import binascii as ba


def block_hash(item):
    block_string = json.dumps(item, sort_keys=True).encode()

    return hashlib.sha256(block_string).hexdigest()


def merkle_hash(a, b):
    a1 = ba.unhexlify(a)[::-1]
    b1 = ba.unhexlify(b)[::-1]
    h = hashlib.sha256(hashlib.sha256(a1 + b1).digest()).digest()

    return ba.hexlify(h[::-1]).decode()


def merkle_root(hash_list):
    if len(hash_list) == 1:
        return hash_list[0]
    if len(hash_list) == 0:
        return ''

    new_hash_list = []

    for i in range(0, len(hash_list) - 1, 2):
        new_hash_list.append(merkle_hash(hash_list[i], hash_list[i + 1]))

    if len(hash_list) % 2 == 1:  # odd, hash last item twice
        new_hash_list.append(merkle_hash(hash_list[-1], hash_list[-1]))

    return merkle_root(new_hash_list)


def goal():
    return "".join(['0'] * g.BLOCKCHAIN_DIFFICULTY)


def valid_proof(last_proof, proof):
    guess = f'{last_proof * proof / (last_proof/(proof + 1))}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:g.BLOCKCHAIN_DIFFICULTY] == goal()