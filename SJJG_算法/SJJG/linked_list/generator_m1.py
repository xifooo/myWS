# generator 实现单链表
class Node:
    def __init__(self,name):
        self.name = name
        self.next = None
        
    def __iter__(self):    # iterable
        Node = self
        while Node is not None:
            yield Node
            Node = Node.next
            
            
node1 = Node('node1')
node2 = Node('node2')
node3 = Node('node3')
node1.next = node2
node2.next = node3

for node in node1:
    print(node.name)