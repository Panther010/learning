from mypy.message_registry import TYPE_ALWAYS_TRUE


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

    def print_list(self):
        temp = self.head
        while temp is not None:
            print(temp.value, end=" --> ")
            temp = temp.next

    def append(self, value):
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
        else:
            temp = self.head
            for _ in range(index):
                temp = temp.next

            return temp

    def set(self, index, value):
        temp = self.get(index)

        if temp:
            temp.value = value
            return True
        return False

    def insert(self, index, value):
        new_node = Node(value)

        if self.length == 0:
            return self.prepend(value)
        if self.length == index:
            return self.append(value)

        prev = self.get(index-1)
        new_node.next = prev.next
        prev.next = new_node

        self.length += 1
        return True

    def remove(self, index):

        if self.length == 0:
            return self.pop_first()
        if self.length == index:
            return self.pop

        prev = self.get(index-1)
        temp = prev.next
        prev.next = temp.next
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

    def find_middel_node(self):
        slow = self.head
        fast = self.head

        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

        return slow

    def has_loop(self):
        slow = self.head
        fast = self.head

        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True

        return False

    def find_kth_from_end(self, value):
        slow = fast = self.head

        for _ in range(value):
            if fast is None:
                return None
            fast = fast.next

        while fast:
            slow = slow.next
            fast = fast.next

        return slow

    def remove_duplicates(self):
        current = self.head

        while current:
            runner = current
            while runner:
                if current.value == runner.next.value:
                    runner.next = runner.next.next
                    self.length -= 1
                else:
                    runner = runner.next

            current = current.next

    def binary_to_decimal(self):
        result = 0
        temp = self.head

        while temp:
            result = 2 * result + temp.value
            temp = temp.next

        return result

    def make_empty(self):
        self.head = None
        self.tail = None
        self.length = 0

    def partition_list(self, x):
        dummy1 = Node(None)
        dummy2 = Node(None)

        lesser = dummy1
        greater = dummy2

        temp = self.head

        while temp:
            if temp.value < x:
                lesser.next = temp
                lesser = lesser.next
            else:
                greater.next = temp
                greater = greater.next

            temp = temp.next

        greater.next = None
        self.tail = greater.next

        lesser.next = dummy2.next
        self.head = dummy1.next








