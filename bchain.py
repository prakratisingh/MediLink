
import json
import hashlib
import os

# MedBlockchain class
class MedBlockchain:
    # constructor of the class 
    def __init__(self):
        # creating blockchain.json if it do not exists
        if not os.path.exists('blockchain.json'):
            # opened the file in writing format
            with open('blockchain.json', 'w') as file:
                # inserting empty json 
                data = {}
                json.dump(data, file)
    
    # function to calculate hash for that particular block
    def calculateHash(self,block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    # function to open the json file in reading mode
    def loadBlockchain(self):
        with open('blockchain.json', 'r') as file:
            return json.load(file)
        
    # function to save the new block added against that user
    def saveBlockchain(self,blockchain):
        with open('blockchain.json', 'w') as file:
            json.dump(blockchain, file)

    # function to create a block
    def createBlock(self,username, medicine, date):
        block = {
            'medicine': medicine,
            'date': date
        }

        blockchain = self.loadBlockchain()
        user_chain = blockchain.get(username, [])
        # getting the last block if it exists otherwise None
        previous_block = user_chain[-1] if user_chain else None

        if previous_block:
            block['previous_hash'] = self.calculateHash(previous_block)
        else:
            block['previous_hash'] = None

        # block['hash'] = calculate_hash(block)
        user_chain.append(block)
        # updating the chain of that user
        blockchain[username] = user_chain

        self.saveBlockchain(blockchain)
        # returning the hash code of the new block
        return self.calculateHash(block)
    
    # function to get the chain of that user
    def getUserBlocks(self,username):
        blockchain = self.loadBlockchain()
        return blockchain.get(username, None)

    # function to check integrity of the user's chain 
    def checkIntegrity(self,username,lastHash):
        userBlock = self.getUserBlocks(username)

        if not userBlock:
            return False

        j = len(userBlock)
        # comparing the hash of the previous block withe current block's previous hash key
        while j>0:
            if j==len(userBlock):
                if lastHash!=self.calculateHash(userBlock[j-1]):
                    return False
            else:
                if userBlock[j]['previous_hash'] != self.calculateHash(userBlock[j-1]):
                    return False
            
            j = j - 1

        return True