class QueueUsingTwoStack:

    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def size(self, stack):
        return len(stack)

    def is_empty(self, stack):
        return self.size(stack) == 0

    def enqueue(self, value):
        self.in_stack.append(value)

    def dequeue(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

        if self.is_empty(self.out_stack):
            return "Queue is empty"

        return self.out_stack.pop()

    def peek(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

        if self.is_empty(self.out_stack):
            return "Queue is empty"

        return self.out_stack[-1]

    def __str__(self):
        """String representation of the queue."""
        return str(self.out_stack[::-1] + self.in_stack)


# Test the QueueUsingTwoStack class
if __name__ == "__main__":
    queue = QueueUsingTwoStack()
    queue.enqueue(1)
    print(queue)
    queue.enqueue(2)
    print(queue)
    queue.enqueue(3)
    print(queue)

    print("Dequeued:", queue.dequeue())  # Should print 1
    print("Dequeued:", queue.dequeue())  # Should print 2

    queue.enqueue(4)
    print(queue)
    print("Dequeued:", queue.dequeue())  # Should print 3
    print("Dequeued:", queue.dequeue())  # Should print 4

    print("Dequeued:", queue.dequeue())
