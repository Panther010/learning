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


    def print_list(self):
        """
        for printing list will start from head and will go till tail
        """
        temp = self.head
        while temp:
            print(temp.value, end = " --> ")
            temp = temp.next

    def append(self, value):
        """
        append at the end of the list. first create the node with value.
        If this is the only node this will be head and tail both otherwise this will be tail length +1
        """
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
        """
        Remove the last value from the Linked List
        if length == 0 cant remove
        go to second last element and make it tail. length -1. Inc ase now length is zero mark head and tail None
        """
        if self.length == 0:
            return None

        temp = prev = self.head

        while temp.next:
            prev = temp
            temp = temp.next

        prev.next = None
        self.tail = prev
        self.length -= 1

        if self.length == 0:
            self.head = None
            self.tail = None

        return prev


    def prepend(self, value):

        """
        Add the node at the beginning of the List
        if this is the only element it will be both head and tail
        or else it will replace head and length +1
        """
        pass


    def pop_first(self):
        """
        Remove first element
        if there is no element cant remove return None
        otherwise replace head with next element length -1. If ater this length is 0 mark head and tail None
        """
        pass


    def get(self, index):
        pass


    def set(self, index, value):
        pass


    def insert(self, index, value):
        pass


    def remove(self, index):
        pass



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









