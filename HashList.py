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