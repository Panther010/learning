class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def _is_empty(self):
        return self.head is None

    def append(self, value):
        new_node = Node(value)
        if self._is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def prepend(self, value):
        new_node = Node(value)
        if self._is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.head.prev = new_node
            new_node.next = self.head
            self.head = new_node

    def delete(self, value):
        if self._is_empty():
            print("List is empty")
            return

        current = self.head
        while current:
            if current.value == value:
                if self.head == current and self.tail == current:
                    self.head = None
                    self.tail = None
                elif self.head == current:
                    self.head = current.next
                    self.head.prev = None
                elif self.tail == current:
                    self.tail = current.prev
                    self.tail.next = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                return

            current = current.next

        print(f"Value {value} not present in the list")

    def search(self, value):
        if self._is_empty():
            return False

        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next

        return False

    def print_list(self):
        if self._is_empty():
            print("List is empty")

        current = self.head

        while current:
            print(current.value, end=" <--> ")
            current = current.next
        print("None")

    def print_reverse(self):
        if self._is_empty():
            print("List is empty")

        current = self.tail

        while current:
            print(current.value, end=" <--> ")
            current = current.prev
        print("None")


# Example Usage
if __name__ == "__main__":
    dll = DoublyLinkedList()

    # Prepend elements
    dll.prepend(3)
    dll.prepend(2)
    dll.prepend(1)

    # Append elements
    dll.append(4)
    dll.append(5)

    # Print the list
    print("List from head to tail:")
    dll.print_list()  # Expected: 1 <-> 2 <-> 3 <-> 4 <-> 5 <-> None

    # Print the list in reverse
    print("List from tail to head:")
    dll.print_reverse()  # Expected: 5 <-> 4 <-> 3 <-> 2 <-> 1 <-> None

    # Search for an element
    print(dll.search(3))  # True
    print(dll.search(10))  # False

    # Delete an element
    print("Delete 3 from the list:")
    dll.delete(3)
    dll.print_list()  # Expected: 1 <-> 2 <-> 4 <-> 5 <-> None

    # Try deleting an element not in the list
    dll.delete(10)  # Should print that value 10 is not found
