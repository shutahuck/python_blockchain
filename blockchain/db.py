import json
import binascii
import strings as s


def get_blockchain():
    try:
        with open(s.DB_FILE_NAME, "rb") as file:
            chain = json.loads(binascii.unhexlify(file.read()).decode())['chain']
    except BaseException:
        chain = []

    message = s.NEW_CHAIN_CREATED_MSG if len(chain) == 0 else s.CHAIN_LOADED_MSG + str(len(chain))
    print(message)

    return chain


def save_blockchain(chain):
    blockchain = {
        'chain': chain,
        'length': len(chain)
    }

    with open(s.DB_FILE_NAME, "wb") as file:
        file.write(binascii.hexlify(json.dumps(blockchain, ensure_ascii=False).encode("utf-8")))
        message = s.CHAIN_SAVED_MSG + str(len(chain))
        print(message)



'''
    try:
        with open(s.TEMP_FILE_NAME, "w") as file:
            file.write(json.dumps(blockchain, ensure_ascii=False))

        with open(s.TEMP_FILE_NAME, "rb") as file:
            binary_data = file.read()

        open(s.TEMP_FILE_NAME, 'w').close()

    except BaseException:
        print(s.BASE_EXCEPTION_ERR)

    try:
        with open(s.DB_FILE_NAME, "wb") as file:
            file.write(binascii.hexlify(binary_data))
            message = s.CHAIN_SAVED_MSG + str(len(chain))
            print(message)

    except FileNotFoundError:
        print(s.FILE_NOT_FOUND_ERR)
'''