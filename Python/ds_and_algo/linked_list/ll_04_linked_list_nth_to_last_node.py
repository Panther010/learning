class Node:

    def __init__(self, val):

        self.value = val
        self.next = None


class SinglyLinkedList:

    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def append(self, val):
        new_node = Node(val)

        if self.is_empty():
            print("list is empty")
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = new_node

    def prepend(self, val):
        new_node = Node(val)
        new_node.next = self.head
        self.head = new_node

    def delete(self, val):
        if self.is_empty():
            print("list is empty")
            return

        current = self.head

        if current.value == val:
            self.head = current.next

        while current.next and current.next.value != val:
            current = current.next

        if current.next is None:
            print(f"value {val} is not present in the list")
        else:
            current.next = current.next.next

    def search(self, val):
        if self.is_empty():
            print("list is empty")
            return

        current = self.head

        while current:
            if current.value == val:
                return True
            current = current.next

        return False

    def __str__(self):
        if self.is_empty():
            print("list is empty")
            return

        current = self.head
        count = 0

        while current:
            print(current.value, end='-->')
            current = current.next
            if count > 100:
                return "Seems like there is a cycle in the list"
            count += 1

        return ""

    def add_cyclic(self, position):
        if self.is_empty():
            print("list is empty")
            return

        pos = last = self.head

        while last.next:
            last = last.next

        count = 1

        while pos.next and count < position:
            pos = pos.next
            count += 1

        if pos.next is None:
            print("Position is not present in the list")

        last.next = pos

    def cyclic_check(self):
        if self.is_empty():
            print("list is empty")
            return False

        slow = fast = self.head

        while fast and fast.next:

            slow = slow.next
            fast = fast.next.next

            if fast:
                print(f"Slow: {slow.value}, Fast: {fast.value}")
            if slow == fast:
                return True

        return False

    def reversal(self):
        if self.is_empty():
            print("list is empty")
            return

        current = self.head
        previous = None

        while current:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        self.head = previous

    def nth_to_last_node(self, n):
        if self.is_empty():
            print("list is empty")
            return

        left = right = self.head

        for i in range(1, n):
            if not right.next:
                raise ValueError(f"position {n} is bigger than the total length of list")
            right = right.next

        while right.next:
            left = left.next
            right = right.next

        print(left.value)


# Example Usage
if __name__ == "__main__":
    sll = SinglyLinkedList()

    # Prepend elements to the linked list
    sll.prepend(3)
    sll.prepend(2)
    sll.prepend(1)
    print(sll)

    # Append elements to the linked list
    sll.append(4)
    sll.append(5)
    sll.append(6)
    sll.append(7)
    sll.append(8)
    sll.append(9)
    print(sll.search(10))  # False
    sll.append(10)
    print(sll)
    sll.append(11)
    sll.append(12)
    sll.append(13)
    sll.append(14)
    sll.append(15)
    sll.append(16)
    sll.append(17)
    sll.append(18)
    sll.append(19)
    sll.append(20)

    # Print the list
    print(sll)  # Expected: 1 -> 2 -> 3 -> 4 -> 5 ---> 20 ->

    # Search for an element
    print(sll.search(3))  # True
    print(sll.search(10))  # False

    # Delete an element
    sll.delete(3)
    print(sll)  # Expected: 1 -> 2 -> 4 -> 5 ---> 20 -> None

    # Try deleting an element not in the list
    sll.delete(10)
    sll.delete(25)  # Should print that value 25 is not found
    print(sll)

    sll.nth_to_last_node(8)
    print(sll)

    print("checking after reversal")
    sll.reversal()
    print(sll)

    print(sll.cyclic_check())
    sll.add_cyclic(5)
    print(sll)
    print(sll.cyclic_check())
