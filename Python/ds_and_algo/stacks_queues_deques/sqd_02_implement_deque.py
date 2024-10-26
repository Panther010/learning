class Deque:

    def __init__(self):
        self.deque = []

    def size(self):
        return len(self.deque)

    def is_empty(self):
        return self.size() == 0

    def add_front(self, element):
        self.deque.append(element)

    def add_rear(self, element):
        self.deque.insert(0, element)

    def remove_front(self):
        if self.is_empty():
            print('Deque is empty')
            return None
        return self.deque.pop()

    def remove_back(self):
        if self.is_empty():
            print('Deque is empty')
            return None
        return self.deque.pop(0)


# Test the Deque class
if __name__ == "__main__":
    d = Deque()
    d.add_front(10)
    d.add_rear(20)
    d.add_front(30)

    print("Deque size:", d.size())  # Should print 3

    print("Remove front:", d.remove_front())  # Should print 10
    print("Remove back:", d.remove_back())  # Should print 30
    print("Deque size:", d.size())  # Should print 1
