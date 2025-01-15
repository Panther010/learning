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

    def peek_front(self):
        """Returning value from the top of the deque"""
        if self.is_empty():
            return "deque is empty"
        return self.deque[-1]

    def peek_rear(self):
        """Returning value from the bottom of the deque"""
        if self.is_empty():
            return "deque is empty"
        return self.deque[0]

    def __str__(self):
        return str(self.deque)


# Test the Deque class
if __name__ == "__main__":
    # Initialize a deque instance
    d = Deque()

    # Add elements
    d.add_front(10)
    d.add_rear(20)
    d.add_front(30)

    # Assertions for testing
    assert d.size() == 3, "Size should be 3 after adding three elements"
    assert d.remove_front() == 30, "Front element should be 30"
    assert d.remove_back() == 20, "Rear element should be 20"
    assert d.size() == 1, "Size should be 1 after removing two elements"

    # Add more elements and test peeks
    d.add_front(40)
    assert d.peek_front() == 40, "Front element should be 40"
    assert d.peek_rear() == 10, "Rear element should be 10"

    print("All tests passed successfully!")
