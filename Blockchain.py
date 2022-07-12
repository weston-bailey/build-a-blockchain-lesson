import hashlib
import json
from time import time
from pprint import pprint

class Blockchain:
    def __init__(self):
        # list to add blocks to
        self.chain = []
        # list of transactions that have not been added to the chain in a block
        self.pending_transactions = []
        self.new_block(previous_hash="The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.", proof=100)

    # def __str__(self):
    #     return str(self.chain)

    def __len__(self):
        return len(self.chain)

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def proof_algorithm(prev_proof, new_proof):
        return hashlib.sha256(str(new_proof ** 2 - prev_proof ** 2).encode()).hexdigest()

    @staticmethod
    def consensus(*args):
        # remove all chains that do not pass validation
        valid_chains = []
        for chain in args:
            if chain.validate_chain():
                valid_chains.append(chain)

        # if no chains are valid, return false
        if len(valid_chains) == 0:
            return False

        # find the longest chain and return it
        longest_chain = valid_chains[0]

        for chain in valid_chains:
            if len(chain) > len(longest_chain):
                longest_chain = chain

        return longest_chain

    def new_block(self, proof, previous_hash=None):
        # create a new block 
        block = {
            'index': len(self) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block)
        }
        # clear out the pending transactions
        self.pending_transactions = []
        # append the new block to the chain
        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):
        # create a transaction
        transactions = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        # add new transaction to list of pending transactions
        self.pending_transactions.append(transactions)
        return self.last_block['index'] - 1

    def hash(self, block):
        # orders the keys of the block in a predictable way
        string_block = json.dumps(block, sort_keys=True).encode()
        # hash the block
        return hashlib.sha256(string_block).hexdigest()

    def proof_of_work(self, verbose=False):
        # need the prvious proof for our proofing algorithm
        previous_proof = self.last_block['proof']
        # nonce is basically the guess or arbitrary number used to find the proof
        # nonce = number used once 
        nonce = 1
        # loop until a valid nonce/proof is found
        check_proof = False
        while check_proof is False:
            # use our algorithm to check each nonce
            proof_guess = Blockchain.proof_algorithm(previous_proof, nonce)
            # print data as we search
            if verbose:
                print(nonce, 'matches!' if proof_guess[:4] == '0000' else 'does not match')
            # if the proof we guessed starts with four 0000 zeros, it is accurate
            # otherwise keep searching for a new guess
            if proof_guess[:4] == '0000':
               check_proof = True
            else:
                nonce += 1

        # return the number found
        return nonce

    def validate_chain(self):
        # loop over entire chain
        i = 0
        while i <= len(self) - 2:
            # comparing the blocks in groups of two
            prev_block = self.chain[i]
            next_block = self.chain[i + 1]
            print(i, len(self))
            # if the hashes don't line up, there is a mismatch
            if next_block['previous_hash'] != self.hash(prev_block):
                return False

            # check that the hashes match the algorithm
            hash_check = Blockchain.proof_algorithm(prev_block['proof'],
                                                   next_block['proof'])
            # the hash needs to start with four zeros to be valid
            if hash_check[:4] != '0000':
                return False

            i += 1

        # if we make it here, all hashes have checked and passed
        return True


def main():
    # create a blockchain
    bc = Blockchain()
    t1 = bc.new_transaction('bob', 'alice', 10)
    t2 = bc.new_transaction('frank', 'mary', 20)

    # testing proof of work and transactions
    proof = bc.proof_of_work()
    print(proof)


    bc.new_block(bc.proof_of_work(verbose=True))
    t3 = bc.new_transaction('spam', 'eggs', 30)
    t4 = bc.new_transaction('bacon', 'sausage', 15)
    bc.new_block(bc.proof_of_work())
    t5 = bc.new_transaction('ham', 'sausage', 30)
    t6 = bc.new_transaction('bacon', 'sausage', 15)
    pprint(bc.chain)
    print(bc.validate_chain())

    # testing validation
    not_valid = Blockchain()
    not_valid.new_transaction('eggs', 'spam', 30)
    not_valid.new_block(123456)
    old_chain = Blockchain()
    old_chain.chain = bc.chain[:len(bc) - 2]
    current_chain = Blockchain.consensus(bc, not_valid, old_chain)
    pprint(current_chain.chain)

if __name__ == '__main__':
    main()