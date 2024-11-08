class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self, root_value):
        self.root = root_value

    def insert(self, value):
        """In case root is not present given value will be root else fit the value in BST"""
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        """If given value is lesser than the node vale it will go to left side else it will go to right side"""
        if value < node.value:  # value is lesser than the node value
            if node.left is None:  # there is no node present at the left of the Node
                node.left = Node(value)  # add new node to the left of the node
            else:  # Node is already present check one more level below
                self._insert_recursive(node.left, value)
        elif value > node.value:  # value is greater than the node value
            if node.right is None:
                node.right = Node(value)  # add new node to the right of the node
            else:
                self._insert_recursive(node.right, value)

    def search(self, value):
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        """Check if an element is present in Tree or not.
        Start from root if value is smaller than node value move left
        otherwise move right of the BST"""
        if node.value is None:
            return False
        if node.value == value:
            return True
        if value < node.value:
            self._search_recursive(node.left, value)
        if value > node.value:
            self._search_recursive(node.right, value)

    def pre_order_traversal(self, node, values=None):
        if values is None:
            values = []

        if node:
            values.append(node.value)
            self.pre_order_traversal(node.left, values)
            self.pre_order_traversal(node.right, values)

    def in_order_traversal(self, node, values=None):
        if values is None:
            values = []

        if node:
            self.in_order_traversal(node.left, values)
            values.append(node.value)
            self.in_order_traversal(node.right, values)

    def post_order_traversal(self, node, values=None):
        if values is None:
            values = []

        if node:
            self.post_order_traversal(node.left, values)
            self.post_order_traversal(node.right, values)
            values.append(node.value)



