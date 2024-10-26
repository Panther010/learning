def size(a):
    return len(a)


def is_empty(a):
    return size(a) == 0


class QueueUsingTwoStack:

    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def enqueue(self, element):
        self.in_stack.append(element)
        print("In stack ", self.in_stack)

    def dequeue(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

        print("Out stack ", self.out_stack)
        if is_empty(self.out_stack):
            print('Queue is empty')
            return None

        return self.out_stack.pop()


# Test the QueueUsingTwoStack class
if __name__ == "__main__":
    queue = QueueUsingTwoStack()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)

    print("Dequeued:", queue.dequeue())  # Should print 1
    print("Dequeued:", queue.dequeue())  # Should print 2

    queue.enqueue(4)
    print("Dequeued:", queue.dequeue())  # Should print 3
    print("Dequeued:", queue.dequeue())  # Should print 4

    print("Dequeued:", queue.dequeue())