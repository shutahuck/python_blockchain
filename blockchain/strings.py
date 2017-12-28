#CONSTANTS
DB_FILE_NAME = "blockchain_data.bch"
TEMP_FILE_NAME = "temp.bch"
TEMP_FILE_NAME1 = "temp1.bch"
NODE_IDENTIFIER = "9bc9237486734ed2b5ca4330055db8be-3k2l5m"
MY_WALLET_IDENTIFIER = '8def1149f4744cc7969973e4b133d299'
BLOCK_REWARD = 12.5
GENERATED_BLOCK = "Newly Generated Coins"
BLOCKCHAIN_DIFFICULTY = 4
BLOCK_HASH_KEYS = ['timestamp', 'merkle_root', 'proof', 'previous_hash']


#ERRORS
FILE_NOT_FOUND_ERR = "File not found!"
BASE_EXCEPTION_ERR = "Ooops! Something went wrong!"
INVALID_NODES_LIST_ERR = "Error: Please supply a valid list of nodes"


#ROUTES
MINE_ROUTE = '/mine'
NEW_TRANSACTION_ROUTE = '/transactions/new'
FULL_CHAIN_ROUTE = '/chain'
NODE_REGISTER_ROUTE = '/nodes/register'
RESOLVE_CONFLICTS_ROUTE = '/nodes/resolve'


#MESSAGES
NEW_CHAIN_CREATED_MSG = "New chain was created successfully."
NEW_BLOCK_CREATED_MSG = "New block was created successfully. Block index is "
CHAIN_LOADED_MSG = "Existed chain was loaded successfully. Last block index is "
CHAIN_SAVED_MSG = "Chain was saved successfully. Last block index is "
CHAIN_REPLACED_MSG = "Our chain was replaced"
CHAIN_NOT_REPLACED_MSG = "Our chain is authoritative"
NEW_NODES_ADDED_MSG = "New nodes have been added"
NEW_BLOCK_FORGED_MSG = "New Block Forged"

