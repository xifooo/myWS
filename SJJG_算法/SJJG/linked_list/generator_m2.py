class Node_iter:    # 链表
    def __init__(self, Node) -> None:
        self.cur_node = Node
        
    def __next__(self):    # iterator
        if self.cur_node is None:
            raise StopIteration
        Node, self.cur_node = self.cur_node, self.cur_node.next
        return Node
    
    def __iter__(self):    # iterable
        return self
        

class Node:    # 节点
    def __init__(self, name) -> None:
        self.name = name
        self.next = None
    
    def __iter__(self):    # iterable
        return Node_iter(self)
    
    
node1 = Node('node1')
node2 = Node('node2')
node3 = Node('node3')
node1.next = node2
node2.next = node3

for node in node1:
    print(node.name)