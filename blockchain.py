# create blockchain - module 


# import the libraries 

# import datetime
import datetime

# import hashlib
import hashlib

# import json
import json

# from flask From Flask, jsonify
from flask import Flask, jsonify


# part 1- building a blockchain

class Blockchain:
    
    # initial value
    def __init__(self):
        
        #create a chain
        self.chain = [] # That list it's list of blocks 
        
        # create a genesis block
        self.create_block(proof = 1, previous_hash = '0')

    
    # function for create blocks
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            }
        self.chain.append(block) # added to chain list
        return block

    # get previous block function
    def get_previous_block(self):
        return self.chain[-1]
    
    
    # proof of work function
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()               
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        
        return new_proof

    # hash function to verify is previous hash is right
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    #check a chain is vaild
    def is_chain_vaild(self, chain):
        previous_block = chain[0] 
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index] # current block
            if block['previous_hash'] != self.hash(previous_block):
                return False
            # check the proof
            previous_proof = previous_block['proof']
            proof = block['proof'] # current proof - current block
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block
            block_index += 1
        return True
            

# Mining our blockchain - module

# create a web app
app = Flask(__name__)

# If Get Error with flask run
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


#get a inital value - object
blockchain = Blockchain()



# mining a new block
@app.route('/mine_block', methods=['GET'])


#mine block
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    
    response = {
        'message': 'Congratulations, you just mined a block',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
        }
    return jsonify(response), 200

# getting the ful blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
        }
    return jsonify(response), 200

# is blockchain is valid
@app.route('/is_valid', methods=['GET'])

def is_valid():
    is_valid = blockchain.is_chain_vaild(blockchain.chain)
    if is_valid :
        response = {
            'message': 'The Blockchain is valid'
            }
    else:
        response = {'message': 'Sorry, The blockchain is not valid'}
    
    
    return jsonify(response), 200

# running the app
app.run(host= '0.0.0.0' , port= 5000)









