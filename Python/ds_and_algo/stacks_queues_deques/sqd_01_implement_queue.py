class Queue(object):

    def __init__(self):
        self.queue = []

    def size(self):
        return len(self.queue)

    def is_empty(self):
        return self.size() == 0

    def enqueue(self, element):
        self.queue.append(element)

    def dequeue(self):
        if self.is_empty():
            print(f"Queue is empty")
            return None
        return self.queue.pop(0)

    def peek(self):
        if self.is_empty():
            print('Queue is empty')
            return None
        return self.queue[0]


# Testing the Queue class
if __name__ == "__main__":
    queue = Queue()
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)

    print("Front item:", queue.peek())
    print("Queue size:", queue.size())

    queue.dequeue()
    print("After dequeue, front item:", queue.peek())

    queue.dequeue()
    queue.dequeue()

    print("Is queue empty?", queue.is_empty())