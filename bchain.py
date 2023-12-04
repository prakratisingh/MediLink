import json
import hashlib
import os

class MedBlockchain:
    def __init__(self):
        if not os.path.exists('blockchain.json'):
            with open('blockchain.json', 'w') as file:
                data = {}
                json.dump(data, file)
    
    def calculateHash(self,block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def loadBlockchain(self):
        with open('blockchain.json', 'r') as file:
            return json.load(file)
    
    def saveBlockchain(self,blockchain):
        with open('blockchain.json', 'w') as file:
            json.dump(blockchain, file)

    def createBlock(self,username, medicine, date):
        block = {
            'medicine': medicine,
            'date': date
        }

        blockchain = self.loadBlockchain()
        user_chain = blockchain.get(username, [])

        previous_block = user_chain[-1] if user_chain else None

        if previous_block:
            block['previous_hash'] = self.calculateHash(previous_block)
        else:
            block['previous_hash'] = None

        # block['hash'] = calculate_hash(block)
        user_chain.append(block)
        blockchain[username] = user_chain

        self.saveBlockchain(blockchain)
        return self.calculateHash(block)
        
    def getUserBlocks(self,username):
        blockchain = self.loadBlockchain()
        return blockchain.get(username, None)

    def checkIntegrity(self,username,lastHash):
        userBlock = self.getUserBlocks(username)

        if not userBlock:
            return False
        
        j = len(userBlock)
        while j>0:
            if j==len(userBlock):
                if lastHash!=self.calculateHash(userBlock[j-1]):
                    return False
            else:
                if userBlock[j]['previous_hash'] != self.calculateHash(userBlock[j-1]):
                    return False
            
            j = j - 1

        return True