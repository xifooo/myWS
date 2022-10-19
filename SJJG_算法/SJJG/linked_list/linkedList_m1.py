class node:
    def __init__(self, name=None, next=None):
        self.name = name
        self.next = next      
        
node1 = node(1)
node2 = node(2)
node3 = node(3)

node1.next = node2
node2.next = node3

print(node1.next)
