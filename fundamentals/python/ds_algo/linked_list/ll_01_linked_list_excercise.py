class Node:
    def __init__(self, value):
        """
        A single node with value and pointing nowhere/ None
        """
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self, value):
        """
        Linked list with single node here single node wil be head, tail and length will be one
        """
        new_node = Node(value)
        self.head = new_node
        self.tail = new_node
        self.length = 1


    def print_list(self) -> None:
        """
        for printing list will start from head and will go till tail
        """
        temp_node = self.head
        while temp_node:
            print(temp_node.value, ' => ', end='')
            temp_node = temp_node.next

    def append(self, value) -> bool:
        """
        append at the end of the list. first create the node with value.
        If this is the only node this will be head and tail both otherwise this will be tail length +1
        """
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self.length += 1
        return True

    def pop(self) -> Node | None:
        """
        Remove the last value from the Linked List
        if length == 0 cant remove
        go to second last element and make it tail. length -1. Inc ase now length is zero mark head and tail None
        """
        if self.length == 0:
            return None

        temp_node = self.head
        pre = self.head

        while temp_node.next:
            pre = temp_node
            temp_node = temp_node.next

        self.tail = pre
        self.tail.next = None

        self.length -= 1

        if self.length == 0:
            self.head = None
            self.tail = None

        return temp_node

    def prepend(self, value) -> bool:

        """
        Add the node at the beginning of the List
        if this is the only element it will be both head and tail
        or else it will replace head and length +1
        """
        new_node = Node(value)
        if self.length == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next= self.head
            self.head = new_node

        self.length += 1

        return True

    def pop_first(self) -> Node | None:
        """
        Remove first element
        if there is no element cant remove return None
        otherwise replace head with next element length -1. If ater this length is 0 mark head and tail None
        """
        if self.head is None:
            return None

        temp_node = self.head
        self.head = temp_node.next
        temp_node.next = None
        self.length -= 1

        if self.length == 0:
            self.head = None
            self.tail = None

        return temp_node

    def get(self, index) -> None | Node:
        if index >= self.length or index < 0:
            return None

        temp_node = self.head
        for i in range(index):
            temp_node = temp_node.next

        return temp_node

    def set(self, index, value) -> bool:
        temp_node = self.get(index)

        if temp_node:
            temp_node.value = value
            return True

        return False

    def insert(self, index, value) -> bool:

        if index < 0 or index > self.length:
            return False

        if index == 0:
            return self.prepend(value)

        if index == self.length:
            return self.append(value)

        new_node = Node(value)
        temp_node = self.get(index-1)
        new_node.next = temp_node.next
        temp_node.next = new_node
        self.length += 1

        return True

    def remove(self, index) -> None | Node:
        if index < 0 or index >= self.length:
            return None
        if index == 0:
            return self.pop_first()
        if index == self.length - 1:
            return self.pop()

        pre = self.get(index -1)
        temp_node = pre.next

        pre.next = temp_node.next
        temp_node.next = None
        self.length -= 1

        if self.length == 0:
            self.head = None
            self.tail = None

        return temp_node

    def reverse(self):

        temp = self.head
        self.head = self.tail
        self.tail = temp

        before = None

        for _ in range(self.length):
            after = temp.next
            temp.next = before
            before = temp
            temp = after


    def find_middel_node(self) -> Node:
        fast = slow = self.head

        while fast is not None and fast.next:
            fast = fast.next.next
            slow = slow.next
        return slow

    def has_loop(self) -> bool:
        fast = slow = self.head

        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
            if fast == slow:
                return True
        return False


    def find_kth_from_end(self, index) -> Node | None:
        if index < 0:
            return None

        fast = slow = self.head

        for _ in range(index):
            if not fast:
                return None
            fast = fast.next

        while fast:
            fast = fast.next
            slow = slow.next

        return slow


    def remove_duplicates(self):
        current = self.head
        while current:
            temp = current
            while temp.next:
                if current.value == temp.next.value:
                    temp.next = temp.next.next
                    self.length -= 1
                else:
                    temp = temp.next

            current = current.next

    def binary_to_decimal(self) -> int:
        result = 0
        temp = self.head

        while temp:
            result = 2 * result + temp.value
            temp = temp.next

        return result



    def make_empty(self):
        pass


    def partition_list(self, x):
        pass





if __name__ == "__main__":
    print("--- 1. Initialize List ---")
    sll = LinkedList(10)
    sll.print_list()  # Expected: 10 --> None

    print("\n\n--- 2. Test append() ---")
    sll.append(20)
    sll.append(30)
    sll.append(40)
    sll.append(50)
    sll.append(60)
    sll.append(70)
    sll.append(80)
    sll.append(90)
    sll.append(80)
    sll.append(70)
    sll.append(60)
    sll.append(50)
    sll.append(40)
    sll.append(30)
    sll.print_list()  # Expected: 10 --> 20 --> 30 --> None

    print("\n\n--- 3. Test prepend() ---")
    sll.prepend(5)
    sll.print_list()  # Expected: 5 --> 10 --> 20 --> 30 --> None

    print("\n\n--- 4. Test pop() ---")
    popped_node = sll.pop()
    print(f"Popped value: {popped_node.value if popped_node else None}")  # Expected: 30
    sll.print_list()  # Expected: 5 --> 10 --> 20 --> None

    print("\n\n--- 5. Test pop_first() ---")
    popped_first = sll.pop_first()
    print(f"Popped first value: {popped_first.value if popped_first else None}")  # Expected: 5
    sll.print_list()  # Expected: 10 --> 20 --> None

    print("\n\n--- 6. Test get() ---")
    node_at_1 = sll.get(1)
    print(f"Value at index 1: {node_at_1.value if node_at_1 else None}")  # Expected: 20

    print("\n--- 7. Test set_value() index 1 val 25 ---")
    sll.set(1, 25)
    sll.print_list()  # Expected: 10 --> 25 --> None

    print("\n\n--- 8. Test insert() index 1 val 15 ---")
    sll.insert(1, 15)  # Insert in the middle
    sll.print_list()  # Expected: 10 --> 15 --> 25 --> None

    print("\n\n--- 9. Test remove() index 1 ---")
    removed_node = sll.remove(1)  # Remove from the middle
    print(f"Removed value: {removed_node.value if removed_node else None}")  # Expected: 15
    sll.print_list()  # Expected: 10 --> 25 --> None

    print("\n\n--- 10. Test reverse() ---")
    sll.reverse()
    sll.print_list()  # Expected: 25 --> 10 --> None

    print("\n\n--- 11. Test middle node() ---")
    middle_node = sll.find_middel_node()
    print(f"Middle to of list is {middle_node.value}")  # Expected: 25 --> 10 --> None

    print("\n\n--- 13. Test find_kth_from_end index = 5 ---")
    kth_value = sll.find_kth_from_end(5)
    print(f"kth value from end to of list is {kth_value.value}")  # Expected: 25 --> 10 --> None

    print("\n\n--- 14. Remove duplicate ---")
    sll.remove_duplicates()
    sll.print_list()
