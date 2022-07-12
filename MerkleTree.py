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