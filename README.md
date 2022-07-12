# Build a Blockchain,
### _or how I learned to stop worrying and love the web3_

## Learning Objectives

* review concepts related to cryptographic hashing
* understand the purpose and implementation of cryptographic datastructures
* understand some practical applications of cryptographic datastructures, and apply knowledge of familiar datastructures to cryptograhic datastructures
* describe the history of the web (web 1.0 and web 2.0), and understand some of the concepts of 'web3'
* understand the difference between a 'blockchain' (public ledger) and other technologies that use cryptographic datastructures
* get practical experience building a simple blockchain

## Prerequisites

* cryptographic hashing/auth
* algorithms
* datastructures including linked lists and binary search trees

## What is a web3?

* Blockchains are ledgers that keep track of transactions, and use cytpographic techniques for data integrity and validation
    * They are a long list of transactions, and anyone can add a transaction, and anyone can see all the transactions. 
    * the information is validated through 'consensus' by third parites (miners) that have to do 'computational work' or 'proofs of work', which is similar computationally to cracking passwords. One block is designed to take 10 minutes to mine
    * created by mysterious 'Satoshi Nakamoto' https://en.wikipedia.org/wiki/Satoshi_Nakamoto
    * there is debate about the exact meaning of blockchain, its a pretty hype-y term
        * how can we decide if git is a blockchain if we can't define exactly what makes a blockchain unique? https://stackoverflow.com/questions/46192377/why-is-git-not-considered-a-block-chain
        *  conssensus and proof of work make blockchain 'decentralized'
* web3 is the notion that 'blockchain' will revolution the technology and infrastructure of the internet
* talk about web 1.0 (dawn of web+) -- user mainly consuming static content (libraries, bbs)
* talk about web 2.0 (2000s+ era)
    * Web 2.0 (also known as participative (or participatory)[1] web and social web)[2] refers to websites that emphasize user-generated content, ease of use, participatory culture and interoperability (i.e., compatibility with other products, systems, and devices) for end users. 
    * https://en.wikipedia.org/wiki/Web_2.0
* talk about web 3.0 (semantic web -- copncept/WIP)
    * The Semantic Web, sometimes known as Web 3.0 (not to be confused with Web3), is an extension of the World Wide Web through standards[1] set by the World Wide Web Consortium (W3C). The goal of the Semantic Web is to make Internet data machine-readable. 
    * standardization
    * IoT
    * https://en.wikipedia.org/wiki/Semantic_Web 
* web3 technically uses no novel technologies (as you will see) but seeks to apply familiar technologies in novel ways
    * solution without a problem
* familiar technologies such as git and bit torrent use the same technologies
* does web3 describe a trend that has been ongoing since the dawn of the web?
* is it novel applications of old techniques? 
* is it nothing new?
* or is it just buzzwords used by non technical 'bitcoin bros' ie people with enough disposable income to dumb disposable income in extremely conjectural technologies/investments with no worry
* how can web get more 'decentralized'?
* would 'web3' just be a shift from silicone valley having all the cards to invenstment banker bitcoin bros taking some?
* how can blockchain save us when the big companies can just buy up whatever new tech looks promising? (ex: Microsoft owns github)

## Hashing using sha256

### What is a hashin funciton? 

[from wikipedia](https://en.wikipedia.org/wiki/Cryptographic_hash_function):

A cryptographic hash function (CHF) is a mathematical algorithm that maps data of an arbitrary size (often called the "message") to a bit array of a fixed size (the "hash value", "hash", or "message digest"). 

It is a one-way function, that is, a function for which it is practically infeasible to invert or reverse the computation. Ideally, the only way to find a message that produces a given hash is to attempt a brute-force search of possible inputs to see if they produce a match, or use a rainbow table of matched hashes. Cryptographic hash functions are a basic tool of modern cryptography.

> A cryptographic hash function must be deterministic, meaning that the same message always results in the same hash. Ideally it should also have the following properties:
> * it is quick to compute the hash value for any given message
> * it is infeasible to generate a message that yields a given hash value (i.e. to reverse the process that generated the given hash value)
> * it is infeasible to find two different messages with the same hash value
> * a small change to a message should change the hash value so extensively that a new hash value appears uncorrelated with the old hash value (avalanche effect)


### SHA256

SHA-2 (Secure Hash Algorithm 2) is a set of cryptographic hash functions designed by the United States National Security Agency (NSA) and first published in 2001.

* SHA-256 is a hash function computed with eight 32-bit words.
* SHA-256 will always output the same hash from the same string, unlike bcrypt which adds salt by default

### Cryptographic vs non cryptographic hashes

* cryptographic hashes, such as the ones used to secured passwords in a database provide a high level of security
* not all hash algorithms are cryptographically secure, but they still have an aboundance of other uses
    * A hash function is any function that can be used to map data of arbitrary size to fixed-size values. The values returned by a hash function are called hash values, hash codes, digests, or simply hashes. The values are usually used to index a fixed-size table called a hash table. Use of a hash function to index a hash table is called hashing or scatter storage addressing. 
    * useful for hash tables and encoding data
    * https://security.stackexchange.com/questions/214656/cryptographic-hash-function-vs-non-cryptographic-hash-function-examples-and-com

### Making hashes in python

```python
# in hash_test.py
import hashlib
# The encode() method encodes the string, using the specified encoding. If no encoding is specified, UTF-8 will be used.
encode = 'A'.encode()
print(encode)
# hexdigest turns hash object into a hashed string
print(hashlib.sha256(encode).hexdigest())
# notice how every print statement returns the same hash with th same input
print(hashlib.sha256(encode).hexdigest())
print(hashlib.sha256(encode).hexdigest())
print(hashlib.sha256(encode).hexdigest())
```

## Datastructures that use cryptographic hashes

hashing can be applied to datastructures, what are the benifits?

* dataintegrity
    * check sums use algorithms like `CRC32`
    * hash tables use pretty simple algorithms
        * `h(k) = k mod n` Here, h(k) is the hash value obtained by dividing the key value k by size of hash table n using the remainder. It is best that n is a prime  number as that makes sure the keys are distributed with more uniformity. 
    * similar to jwts
* data security
    * can hide data
    * similar to jwts being signed
* visualize a list being hashed with miro

```python
# in HashList.py
import hashlib

class Node:
    def __init__(self, value, previous_hash='head'):
        self.value = value
        self.previous_hash = previous_hash
        self.next = None
        self.hash = Node.make_hash(self.value, self.previous_hash)

    def __str__(self):
        return f'{self.hash} : {self.value}\n'

    @staticmethod
    def make_hash(value, previous_hash):
        # hash together the previous hash, the value
        history = str(value) + previous_hash
        return hashlib.sha256(history.encode()).hexdigest()

    @staticmethod
    def validate(left_node, right_node):
        if right_node.hash == Node.make_hash(right_node.value, left_node.hash):
            return True
        else:
            return False

# loop a hash list and verify that all nodes are valid
# if so, return True
# if not, return False
def valid_list(head):
    # list only has a head and so must be valid
    if not head.next:
        return True
    # the current node
    current = head
    while current.next:
        if not Node.validate(current, current.next):
            return False
        current = current.next
    return True
        
def main():
    # create a list
    head = Node(0)
    one = Node(1, head.hash)
    head.next = one
    two = Node(2, one.hash)
    one.next = two
    three = Node(3, two.hash)
    two.next = three
    print(head, one, two, three)
    
    # check out validating nodes
    print(Node.validate(one, two)) # True
    print(Node.validate(one, three)) # False
    print(Node.validate(two, three)) # True
    two.value = 500
    print(Node.validate(one, two)) # False
    
    # validate the a whole list
    print(valid_list(Node(10))) # True
    print(valid_list(head)) # True
    three.value = 5000 # mess with the data to invalidate the list
    print(valid_list(head)) # False

if __name__ == '__main__':
    main()
```

### Merkle Trees

In cryptography and computer science, a hash tree or Merkle tree is a tree in which every "leaf" (node) is labelled with the cryptographic hash of a data block, and every node that is not a leaf (called a branch, inner node, or inode) is labelled with the cryptographic hash of the labels of its child nodes. A hash tree allows efficient and secure verification of the contents of a large data structure. A hash tree is a generalization of a hash list and a hash chain.

The concept of a hash tree is named after Ralph Merkle, who patented it in 1979.

#### Merkle Tree Use Cases

* Git, a distributed version control system, is one of the most widely used. It is used to handle projects by programmers from all around the world.
* Interplanetary File System, a peer-to-peer distributed protocol, is another suitable implementation. It's also open-source, allowing computers to join and use a centralized file system.
* It's part of the technique that generates verifiable certificate transparency logs.
* Amazon DynamoDB and Apache Cassandra use it during the data replication process. These No-SQL distributed databases use Merkle trees to control discrepancies.

#### Demo

* Visual merkle tree on miro
* show merkle tree with git
    * every commit changes all hashes to root, so remotes can verify data integrity quickly, while only a few changes are tracked per commit
* show merkle tree as block chain 

https://medium.com/geekculture/understanding-merkle-trees-f48732772199
https://www.simplilearn.com/tutorials/blockchain-tutorial/merkle-tree-in-blockchain

## Blockchain

### visualize

* talk about ledger
* need to talk about proof of work or computational work to replace trust
* need to talk about consensus
* these are the two defining aspects of a blockchain

### build it

* our blockchain will not have a merkle tree for simplicity
* first do everything except proof_algorithm, proof_of_work, validate_chain, and consensus
* second do proof_algorithm, proof_of_work
* third do validate_chain (can be lab)
* fourth do consensus (can be lab)

```python
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
```

## Merkle Tree Implementation 

just for funsies

```python
# a merkle tree in python
import hashlib

class Node:
    def __init__(self, value, left=None, right=None):
        self.left = left
        self.right = right
        self.value = value

    def __str__(self):
        return str(self.value)

    @staticmethod
    def hash(val):
        # stringify value before digest
        val = str(val)
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    @staticmethod
    def double_hash(val):
        return Node.hash(Node.hash(val))

class MerkleTree:
    def __init__(self, values):
        self.root = None
        self.__build_tree(values)

    def __build_tree(self, values):
        leaves = [Node(Node.double_hash(value)) for value in values]
        # duplicate last elem if there is an odd number of values
        if len(leaves) % 2 == 1:
           # leaves.append(leaves[len(leaves)- 1])
           leaves.append(leaves[-1:][0])
        self.root = self.__build_tree_rec(leaves)
        # for leaf in leaves:
        #     print(leaf.value)

    def __build_tree_rec(self, nodes, val=0):
        # if there are only two, create a tree with three nodes 
        if len(nodes) == 2:
            return Node(Node.double_hash(nodes[0].value + nodes[1].value),
                        nodes[0], nodes[1])

        # if there is only one node, duplicate it for hash
        if len(nodes) == 1:
            return Node(Node.double_hash(nodes[0].value + nodes[0].value),
                        nodes[0], nodes[0])
        # split the nodes in half, recursively create tree
        half = len(nodes) // 2
        left = self.__build_tree_rec(nodes[:half])
        right = self.__build_tree_rec(nodes[half:])
        value = Node.double_hash(left.value + right.value)
        return Node(value, left, right)

    def print_tree(self):
        self.__print_tree_rec(self.root)

    def __print_tree_rec(self, node):
        # base case: there is no left or right
        if node != None:
            print(node)
            self.__print_tree_rec(node.left)
            self.__print_tree_rec(node.right)

    def get_root_hash(self):
        return self.root.value

def main():
    # testing the node
    # root = Node('root', Node('left'), Node('right'))
    # print(root.value, root.left.value, root.right.value)
    # root.left.value = Node.hash(root.left.value)
    # root.right.value = Node.hash(root.right.value)
    # root.value = Node.hash(root.left.value + root.right.value)
    # print(root.value, root.left.value, root.right.value)
    nodes = ['left', 'right']
    two_tree = MerkleTree(nodes)
    # two_tree.print_tree()
    nodes = [1, 2, 3, 4, 5, 6]
    even_tree = MerkleTree(nodes)
    even_tree.print_tree()
    nodes = [0, 1, 2, 3, 4, 5, 6]
    odd_tree = MerkleTree(nodes)
    # odd_tree.print_tree()

if __name__ == '__main__':
    main()
```

## Links

Merkle Trees
* https://medium.com/geekculture/understanding-merkle-trees-f48732772199
* https://initialcommit.com/blog/git-bitcoin-merkle-tree

* checksum, data integrity, data authenticity
    * https://en.wikipedia.org/wiki/Checksum 

###### tags: `lessons`