class DeQueueUsingTwoStack:

    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def size(self) -> int:
        return len(self.in_stack) + len(self.out_stack)

    def is_empty(self) -> bool:
        return self.size() == 0

    def add_front(self, value):
        """Adding value to the top of the deque"""
        self.in_stack.append(value)

    def add_rear(self, value):
        """Adding value to the bottom of the deque"""
        self.out_stack.append(value)

    def remove_front(self):
        """Removing value from the top of the deque"""
        if self.is_empty():
            return 'Dequeue is empty'

        if not self.in_stack:
            while self.out_stack:
                self.in_stack.append(self.out_stack.pop())
        return self.in_stack.pop()

    def remove_rear(self):
        """Removing value from the top of the deque"""
        if self.is_empty():
            return 'Dequeue is empty'

        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

        return self.out_stack.pop()

    def peek_front(self):
        """Returning value from the top of the deque"""
        if self.is_empty():
            return 'Dequeue is empty'

        if not self.in_stack:
            while self.out_stack:
                self.in_stack.append(self.out_stack.pop())
        return self.in_stack[-1]

    def peek_rear(self):
        """Returning value from the top of the deque"""
        if self.is_empty():
            return 'Dequeue is empty'

        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
        return self.out_stack[-1]

    def __str__(self):
        return str(self.out_stack[::-1] + self.in_stack)




# Test the QueueUsingTwoStack class
# Test the StackDeque
if __name__ == "__main__":
    d = DeQueueUsingTwoStack()
    d.add_front(10)
    d.add_rear(20)
    d.add_front(30)
    print(d)  # Output: [30, 10, 20]
    print(d.remove_front())  # Output: 30
    print(d.remove_rear())  # Output: 20
    print(d)  # Output: [10]