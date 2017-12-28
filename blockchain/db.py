import json
import binascii
import global_constants as gc

class Database(object):


    def __init__(self, db_file_name=gc.DB_FILE_NAME):

        self.__db_file_name = db_file_name
        try:
            with open(self.__db_file_name, "rb") as file:
                self.__db_chain = json.loads(binascii.unhexlify(file.read()).decode())['chain'] #self.__db_chain = binascii.unhexlify(json.load(file)['chain'])
        except FileNotFoundError:
            self.__db_chain = []
        except ValueError:
            self.__db_chain = []

    def getChain(self):
        if len(self.__db_chain) == 0:
            print("New chain was created successfully.")
        else:
            print("Chain with last index = " + len(self.__db_chain).__str__() + " was loaded successfully.")
        return self.__db_chain

    def saveChain(self, chain):

        blockchain = {
            'chain': chain,
            'length': len(chain)
        }

        try:
            with open(gc.TEMP_FILE_NAME, "w") as file:
                file.write(json.dumps(blockchain, ensure_ascii=False))
        except FileNotFoundError:
            print("File not found!")

        try:
            with open(gc.TEMP_FILE_NAME, "rb") as file:
                binary_data = file.read()

            open(gc.TEMP_FILE_NAME, 'w').close()
        except FileNotFoundError:
            print("File not found!")

        try:
            with open(self.__db_file_name, "wb") as file:
                file.write(binascii.hexlify(binary_data))
                if len(self.__db_chain) == 1:
                    print("Chain with base block was saved successfully.")
                else:
                    print("Chain with last index = " + len(self.__db_chain).__str__() + " was saved successfully.")
        except FileNotFoundError:
            print("File not found!")

        #file.write(json.dumps(blockchain, ensure_ascii=False))
