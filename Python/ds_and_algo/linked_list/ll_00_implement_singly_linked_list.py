"""
create Node, head, empty check, append, prepend , delete, search, print_list
"""


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def append(self, value):
        """Append the node/value at the end of the linked list"""
        new_node = Node(value)

        if self.is_empty():
            self.head = new_node
            return

        current = self.head
        while current.next:  # Traverse till the end of the list
            current = current.next

        current.next = new_node  # Attach the new node at the end

    def prepend(self, value):
        """ Add a node with the given value at the beginning of the list """
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node

    def delete(self, value):
        """ Delete the first occurrence of a node with the given value """
        if self.is_empty():  # empty check
            print("List is empty")
            return

        if self.head.value == value:  # If the node to be deleted is the head node
            self.head = self.head.next
            return

        # Traverse till the end of the list or just before finding the value
        current = self.head
        while current.next and current.next.value != value:
            current = current.next

        if current.next is None:
            print(f"Value {value} is not present in the List")
        else:
            current.next = current.next.next

    def search(self, value):
        """ Search for a node with a given value, return True if found, False otherwise """
        if self.is_empty():
            return False

        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next

        return False

    def print_list(self):
        """ Print the linked list elements """
        if self.is_empty():
            print("List is empty")
            return

        current = self.head
        while current:
            print(current.value, end=" --> ")
            current = current.next

        print("None")


# Example Usage
if __name__ == "__main__":
    sll = SinglyLinkedList()

    # Prepend elements to the linked list
    sll.prepend(3)
    sll.prepend(2)
    sll.prepend(1)

    # Append elements to the linked list
    sll.append(4)
    sll.append(5)

    # Print the list
    sll.print_list()  # Expected: 1 -> 2 -> 3 -> 4 -> 5 -> None

    # Search for an element
    print(sll.search(3))  # True
    print(sll.search(10))  # False

    # Delete an element
    sll.delete(3)
    sll.print_list()  # Expected: 1 -> 2 -> 4 -> 5 -> None

    # Try deleting an element not in the list
    sll.delete(10)  # Should print that value 10 is not found
