class Stack:

    def __init__(self):
        self.stack = []

    def size(self):
        return len(self.stack)

    def is_empty(self):
        return self.size() == 0

    def push(self, element):
        """adding value at the top of the stack"""
        self.stack.append(element)

    def pop(self):
        """removing value from the top of the stack"""
        if self.is_empty():
            print("Stack is empty!")
            return None
        return self.stack.pop()

    def peek(self):
        if self.is_empty():
            print("Stack is empty!")
            return None
        return self.stack[-1]

    def __str__(self):
        return str(self.stack)


# Test the Stack class
if __name__ == "__main__":
    stack = Stack()
    stack.push(10)
    stack.push(20)
    stack.push(30)

    print("Top element is:", stack.peek())  # Should print 30
    print("Stack size is:", stack.size())   # Should print 3

    stack.pop()
    print("After pop, top element is:", stack.peek())  # Should print 20

    stack.pop()
    stack.pop()  # Stack becomes empty
    print("Stack empty?", stack.is_empty())  # Should print True

    # Test popping from an empty stack
    stack.pop()  # Should print "Stack is empty!"
