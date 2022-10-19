def gen(num):
    while num > 0:
        yield num   # _ = yield num
        num -= 1
    return

g = gen(5)
first = next(g)
for i in g:
    print(i)
    
    

# ——————————————————————————
class NodeIter:
    def __init__(self,node) -> None:
        self.curr_node = node
        
    def __next__(self):  
        if self.curr_node is None:
            raise StopIteration
        node, self.curr_node = self.curr_node, self.curr_node.next
        return node
    
    # 加个__iter__ 就是 iterable 了, 通常情况下最好写上，就这两行代码
    def __iter__(self):
        return self
    
class Node:
    def __init__(self,name) -> None:
        self.name = name
        self.next = None
        
    def __iter__(self):
        # return NodeIter(self)
        node = self
        while node is not None:
            yield node
            node = node.next
        
node1 = Node('node1')
node2 = Node('node2')
node3 = Node('node3')
node1.next = node2
node2.next = node3

for node in node1:
    print(node.name)