class Deque:

    def __init__(self):
        self.deque = []

    def size(self):
        return len(self.deque)

    def is_empty(self):
        return self.size() == 0

    def add_front(self, element):
        """Adding value to the top of the deque"""
        self.deque.append(element)

    def add_rear(self, element):
        """Adding value to the bottom of the deque"""
        self.deque.insert(0, element)

    def remove_front(self):
        """Removing value from the top of the deque"""
        if self.is_empty():
            return 'Deque is empty'
        return self.deque.pop()

    def remove_back(self):
        """Removing value from the bottom of the deque"""
        if self.is_empty():
            return "Deque is empty"
        return self.deque.pop(0)

    def peak_front(self):
        """Returning value from the top of the deque"""
        if self.is_empty():
            return "deque is empty"
        return self.deque[-1]

    def peak_rear(self):
        """Returning value from the bottom of the deque"""
        if self.is_empty():
            return "deque is empty"
        return self.deque[0]

    def __str__(self):
        return str(self.deque)


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
