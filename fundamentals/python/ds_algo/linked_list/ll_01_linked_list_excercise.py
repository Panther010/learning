from mypy.message_registry import TYPE_ALWAYS_TRUE
from pyspark.sql.connect.functions import length


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
            print(temp_node.value, ' --> ', end='')
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
        pass


    def find_middel_node(self):
        pass


    def has_loop(self):
        pass


    def find_kth_from_end(self, value):
        pass


    def remove_duplicates(self):
        pass


    def binary_to_decimal(self):
        pass


    def make_empty(self):
        pass


    def partition_list(self, x):
        pass









