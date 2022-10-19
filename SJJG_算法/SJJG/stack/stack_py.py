from collections import deque
# deque: 类似列表的容器，支持在两端快速的追加和删除元素


class Stack:
    def __init__(self) -> None:
        self.stack = deque()
        
    def push(self, data):
        """
        入栈
        :param data:
        :return:
        """
        self.stack.append(data)
        
    def pop(self):
        """
        出栈
        :return:
        """
        return self.stack.pop()
    
    def size(self):
        """
        栈大小
        :return:
        """
        return len(self.stack)
    
    def is_empty(self):
        return self.size() == 0
    
    
if __name__ == '__main__':
    stack = Stack()
    
    stack.push(4)
    stack.push(3)
    stack.push(1)
    
    print(stack.pop())
    print(stack.size())
    