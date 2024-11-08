class Node:
    """Node class to create a node with left and right marker"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self, root_value):
        """Root creation"""
        self.root = Node(root_value)

    def insert_left(self, current_node, value):
        """Insert a new node left side of given node with given value"""
        if current_node.left is None:  # check if there is node present left side of given node
            current_node.left = Node(value)
        else:
            new_node = Node(value)  # create new node
            new_node.left = current_node.left  # Existing node at the left shifted to left of new node
            current_node.left = new_node  # New node fixed as the left of given node

    def insert_right(self, current_node, value):
        """Insert a new node right side of given node with given value"""
        if current_node.right is None:  # check if there is node present right side of given node
            current_node.right = Node(value)
        else:
            new_node = Node(value)
            new_node.right = current_node.right  # Existing node at the right shifted to right of new node
            current_node.right = new_node  # New node fixed as the left of given node

    def pre_order_traversal(self, node, values=None):
        """go through the node root --> left -- > right"""
        if values is None:
            values = []

        if node:  # node value is not none
            values.append(node.value)
            self.pre_order_traversal(node.left, values)
            self.pre_order_traversal(node.right, values)

        return values

    def in_order_traversal(self, node, values=None):
        """go through the node left --> root -- > right"""
        if values is None:
            values = []

        if node:
            self.in_order_traversal(node.left, values)
            values.append(node.value)
            self.in_order_traversal(node.right, values)

        return values

    def post_order_traversal(self, node, values=None):
        """go through the node left --> right -- > root"""
        if values is None:
            values = []

        if node:
            self.post_order_traversal(node.left, values)
            self.post_order_traversal(node.right, values)
            values.append(node.value)

        return values


# Usage Example
tree = BinaryTree(1)             # Root node with value 1
tree.insert_left(tree.root, 2)    # Left child of root
tree.insert_right(tree.root, 3)   # Right child of root
tree.insert_left(tree.root.left, 4)  # Left child of the node with value 2
tree.insert_right(tree.root.left, 5) # Right child of the node with value 2

# Traversals
print("Pre-order Traversal:", tree.pre_order_traversal(tree.root))  # Output: [1, 2, 4, 5, 3]
print("In-order Traversal:", tree.in_order_traversal(tree.root))    # Output: [4, 2, 5, 1, 3]
print("Post-order Traversal:", tree.post_order_traversal(tree.root)) # Output: [4, 5, 2, 3, 1]
