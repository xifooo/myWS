from collections import deque
# deque: 类似列表的容器，支持在两端快速的追加和删除元素


class Doubleque:
    def __init__(self):
        self.queue = deque()
        
    def is_empty(self):
        """
        判断是否为空队列
        :return:
        """
        return len(self.queue) == 0

    def insert_head(self, data):
        """
        从队首插入数据
        :param data:
        :return:
        """
        self.queue.appendleft(data)

    def insert_tail(self, data):
        """
        从队尾插入数据
        :param data:
        :return:
        """
        self.queue.append(data)

    def delete_head(self):
        """
        从队首删除数据
        :return:
        """
        return self.queue.popleft()

    def delete_tail(self):
        """
        从队尾删除数据
        :return:
        """
        return self.queue.pop()

    def size(self):
        """
        返回队列长度
        :return:
        """
        return len(self.queue)
    
    
if __name__ == '__main__':
    dq = Doubleque()

    print(dq.is_empty())
    dq.insert_head(4)
    dq.insert_tail(5)
    dq.insert_tail(6)

    print(dq.delete_head())
    print(dq.delete_tail())

    print(dq.size())