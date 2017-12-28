import json
import strings as s
import binascii
import codecs
from uuid import uuid4
import strings as gc
import collections
'''
arr = ['0'] * 10
#str = "".join(['0'] * 10)
print("".join(['0'] * gc.BLOCKCHAIN_DIFFICULTY))
print(str(uuid4()).replace('-', ''))
'''
chain = [
        {
            "sender": "d4eer4r4rcd394edd974e",
            "recipient": "someo4r4r4r4r",
            "amount": 250,
            "hash": "1577015dabffec71b26913147f1c3205716eee1607e19d01f3c75e23be071bad"
        },
        {
            "sender": "d4eer4r4rcd394edd974e",
            "recipient": "someo4r4r4r4r",
            "amount": 250,
            "hash": "1577015dabffec71b26913147f1c3205716eee1607e19d01f3c75e23be071bad"
        },
        {
            "sender": "d4eer4r4rcd394edd974e",
            "recipient": "someo4r4r4r4r",
            "amount": 2508,
            "hash": "272c1bdd31f0f88f88688fe714f7e54101127829f0deb5aea32d004fd5161c8c"
        },
        {
            "sender": "Newly Generated Coins",
            "recipient": "8def1149f4744cc7969973e4b133d299",
            "amount": 12.5,
            "hash": "5bd530464bb5ee6d2603593297ddd8e4b10c49537380466858232ba524e6a028"
        }
    ]

blockchain = {
    'chain': chain,
    'length': len(chain)
}

with open(s.TEMP_FILE_NAME1, "w") as file:
    file.write(json.dumps(blockchain, ensure_ascii=False))


with open(s.TEMP_FILE_NAME1, "rb") as file:
    binary_data = file.read()

print(type(binary_data))
print(binary_data)
str = json.dumps(blockchain, ensure_ascii=False)
print(type(str))
byte_str = str.encode("utf-8")

print(byte_str)
print(binascii.hexlify(byte_str))

print(binascii.hexlify(binary_data))


'''
for t in new_tran:
    hash.append(t['hash'])

print(hash)

hash2 = [t['hash'] for t in new_tran]
print(hash2[0])
print(binascii.unhexlify(hash2[0]))
print(binascii.hexlify(binascii.unhexlify(hash2[0])))
'''