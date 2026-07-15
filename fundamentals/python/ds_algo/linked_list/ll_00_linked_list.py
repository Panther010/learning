class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self, value):
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1

    def print_ll(self):
        temp = self.head
        while temp is not None:
            print(temp.value, end=" -->")
            temp = temp.next

    def append(self, value) -> bool:
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1
        return True

    def pop(self):
        if self.length == 0:
            return None

        temp = self.head
        pre = self.head
        while temp.next:
            pre = temp
            temp = temp.next

        pre.next = None
        self.tail = pre

        self.length -= 1

        if self.length == 0:
            self.head = None
            self.tail = None

        return temp

    def prepend(self, value):
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.length += 1

        return True

    def pop_first(self):
        if self.length == 0:
            return None

        temp = self.head
        self.head = temp.next
        temp.next = None

        self.length -= 1

        if self.length == 0:
            self.head = None
            self.tail = None

        return temp

    def get(self, index):
        if index < 0 or index >= self.length:
            return None

        temp = self.head
        for _ in range(index):
            temp = temp.next

        return temp

    def set_value(self, index, value):
        temp = self.get(index)
        if temp:
            temp.value = value
            return True
        return False

    def insert(self, index, value):
        if index < 0 or index > self.length:
            return None
        if index == 0:
            return self.prepend(value)
        if index == self.length:
            return self.append(value)
        new_node = Node(value)
        temp = self.get(index - 1)
        new_node.next = temp.next
        temp.next = new_node
        self.length += 1
        return True

    def remove(self, index):
        if index < 0 or index >= self.length:
            return None
        if index == 0:
            return self.pop_first()
        if index == self.length -1:
            return self.pop()

        pre = self.get(index - 1)
        temp = pre.next
        pre.next = temp.next
        temp.next = None
        self.length -= 1

        return temp

    def reverse(self):
        prev = None
        temp = self.head

        while temp:
            next_node = temp.next
            temp.next = prev
            prev = temp
            temp = next_node

        self.tail = self.head
        self.head = prev






if __name__ == "__main__":
    if __name__ == "__main__":
        print("--- 1. Initialize List ---")
        sll = LinkedList(10)
        sll.print_ll()  # Expected: 10 --> None

        print("\n--- 2. Test append() ---")
        sll.append(20)
        sll.append(30)
        sll.print_ll()  # Expected: 10 --> 20 --> 30 --> None

        print("\n--- 3. Test prepend() ---")
        sll.prepend(5)
        sll.print_ll()  # Expected: 5 --> 10 --> 20 --> 30 --> None

        print("\n--- 4. Test pop() ---")
        popped_node = sll.pop()
        print(f"Popped value: {popped_node.value if popped_node else None}")  # Expected: 30
        sll.print_ll()  # Expected: 5 --> 10 --> 20 --> None

        print("\n--- 5. Test pop_first() ---")
        popped_first = sll.pop_first()
        print(f"Popped first value: {popped_first.value if popped_first else None}")  # Expected: 5
        sll.print_ll()  # Expected: 10 --> 20 --> None

        print("\n--- 6. Test get() ---")
        node_at_1 = sll.get(1)
        print(f"Value at index 1: {node_at_1.value if node_at_1 else None}")  # Expected: 20

        print("\n--- 7. Test set_value() ---")
        sll.set_value(1, 25)
        sll.print_ll()  # Expected: 10 --> 25 --> None

        print("\n--- 8. Test insert() ---")
        sll.insert(1, 15)  # Insert in the middle
        sll.print_ll()  # Expected: 10 --> 15 --> 25 --> None

        print("\n--- 9. Test remove() ---")
        removed_node = sll.remove(1)  # Remove from the middle
        print(f"Removed value: {removed_node.value if removed_node else None}")  # Expected: 15
        sll.print_ll()  # Expected: 10 --> 25 --> None

        print("\n--- 10. Test reverse() ---")
        sll.reverse()
        sll.print_ll()  # Expected: 25 --> 10 --> None