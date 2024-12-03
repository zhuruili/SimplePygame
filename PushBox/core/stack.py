class Stack:
    """ 自定义栈类 """
    def __init__(self, limit=5):
        self.stack = []      # 存放元素
        self.limit = limit   # 栈容量极限

    # 向栈推送元素
    def push(self, data):
        """ 向栈推送元素 """
        # 判断栈是否溢出
        if len(self.stack) >= self.limit:
            del self.stack[0]
            self.stack.append(data)
        else:
            self.stack.append(data)

    # 弹出栈顶元素
    def pop(self):
        """ 弹出栈顶元素 """
        if self.stack:
            return self.stack.pop()
        # 空栈不能被弹出
        else:
            return None

    # 查看堆栈的顶部的元素
    def peek(self):
        """ 查看堆栈的顶部的元素 """
        if self.stack:
            return self.stack[-1]

    # 判断栈是否为空
    def is_empty(self): #
        """ 判断栈是否为空 """
        return not bool(self.stack)

    # 判断栈是否满
    def is_full(self):
        """ 判断栈是否满 """
        return  len(self.stack) == 5

    # 返回栈的元素数量
    def size(self):
        """ 返回栈的元素数量 """
        return len(self.stack)

    # 清空栈元素
    def clear(self):
        """ 清空栈元素 """
        self.stack.clear()
