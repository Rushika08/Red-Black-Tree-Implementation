# Class to represent a node of the tree
class Node:
    def __init__(self, value, color="RED"):
        self.value = value      # Node value
        self.color = color      # RED or BLACK
        self.left = None        # Left child
        self.right = None       # Right child
        self.parent = None      # Parent

# Class to represent a red-black tree
class RedBlackTree: 

    # Constructor to initialize the tree
    def __init__(self):
        self.TNULL = Node(value=None, color="BLACK")
        self.root = self.TNULL


    # Function to perform left rotation
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y


    # Function to perform right rotation
    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.TNULL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x


    # Function to fix the red-black tree after insertion
    def fix_insert(self, k):
        while k.parent.color == "RED":                  # If parent is red
            if k.parent == k.parent.parent.right:       # If parent is right child
                u = k.parent.parent.left  # uncle
                if u.color == "RED":                  # If uncle is red
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:                                 # If uncle is black         
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.left_rotate(k.parent.parent)   # Rotate parent's parent
            else:                                       # If parent is left child
                u = k.parent.parent.right  # uncle
                if u.color == "RED":
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "BLACK"           # Set root color to black


    # Function to fix the red-black tree after deletion
    def fix_delete(self, x):
        while x != self.root and x.color == "BLACK":    # If x is not root and color is black
            if x == x.parent.left:
                s = x.parent.right
                if s.color == "RED":
                    s.color = "BLACK"
                    x.parent.color = "RED"
                    self.left_rotate(x.parent)
                    s = x.parent.right
                if s.left.color == "BLACK" and s.right.color == "BLACK":
                    s.color = "RED"
                    x = x.parent
                else:
                    if s.right.color == "BLACK":
                        s.left.color = "BLACK"
                        s.color = "RED"
                        self.right_rotate(s)
                        s = x.parent.right
                    s.color = x.parent.color
                    x.parent.color = "BLACK"
                    s.right.color = "BLACK"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == "RED":
                    s.color = "BLACK"
                    x.parent.color = "RED"
                    self.right_rotate(x.parent)
                    s = x.parent.left
                if s.right.color == "BLACK" and s.left.color == "BLACK":
                    s.color = "RED"
                    x = x.parent
                else:
                    if s.left.color == "BLACK":
                        s.right.color = "BLACK"
                        s.color = "RED"
                        self.left_rotate(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = "BLACK"
                    s.left.color = "BLACK"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "BLACK"


    # Function to insert a new node with a given value
    def insert(self, key):
        node = Node(value=key)
        node.parent = None
        node.value = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = "RED"

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.value < x.value:
                x = x.left
            else:
                x = x.right

        node.parent = y

        # Finding the correct place to insert the node
        if y is None:
            self.root = node
        elif node.value < y.value:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = "BLACK"      # If node is root
            return

        if node.parent.parent is None:
            return

        self.fix_insert(node)


    # Function to delete a node with a given value
    def delete(self, key):
        # Function to replace node with a given node
        def transplant(u, v):
            if u.parent is None:        # If u is root
                self.root = v
            elif u == u.parent.left:    # If u is left child
                u.parent.left = v
            else:
                u.parent.right = v      # If u is right child
            v.parent = u.parent         # Set parent of v to parent of u

        z = self.root
        # Find node to delete
        while z != self.TNULL:        
            if z.value == key:
                break
            elif key < z.value:
                z = z.left
            else:
                z = z.right

        # If node not found
        if z == self.TNULL:
            return

        y = z       # Assign Node to delete to y
        y_original_color = y.color
        if z.left == self.TNULL:        # If left child is TNULL
            x = z.right
            transplant(z, z.right)      # Replace z with right child

        elif z.right == self.TNULL:     # If right child is TNULL
            x = z.left
            transplant(z, z.left)       # Replace z with left child

        else:
            y = self.minimum(z.right)[0]    # Find minimum node in right subtree
            y_original_color = y.color
            x = y.right
            if y.parent == z:           # If y is right child of z
                x.parent = y            # Set parent of x to y
            else:
                transplant(y, y.right)      # Replace y with right child
                y.right = z.right           # Set right child of y to right child of z
                y.right.parent = y          # Set parent of right child of y to y
            transplant(z, y)                # Replace z with y
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "BLACK":     # If original color of y is black
            self.fix_delete(x)              # Fix the tree


    # Search for a node with a given value
    def search(self, key):
        node = self.root
        while node != self.TNULL and key != node.value:
            if key < node.value:
                node = node.left
            else:
                node = node.right
        return node != self.TNULL


    # Find the minimum node
    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node, node.value


    # Find the maximum node
    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node, node.value


    # Print the tree
    def print_tree(self, node, indent="", last=True):
        if node != self.TNULL:
            print(indent, end="")
            if last:                        # If last node
                print("└──", end="")
                indent += "   "
            else:                           # If not last node
                print("├──", end="")
                indent += "│  "
            color = "R" if node.color == "RED" else "B"         # Set color
            print(f"{color}{node.value}")
            self.print_tree(node.right, indent, False)          # Print right subtree
            self.print_tree(node.left, indent, True)            # Print left subtree


if __name__ == "__main__":
    tree = RedBlackTree()

    inputs = list(map(int, input("Enter space-separated values to insert: ").split()))
    for value in inputs:
        tree.insert(value)          # Insert values
    tree.print_tree(tree.root)

    while True:
        operation = input("Enter operation (e.g., Insert 30, Delete 35, Search 40, Max, Min, Quit): ")
        if operation.startswith("Insert"):
            key = int(operation.split()[1])
            tree.insert(key)
            tree.print_tree(tree.root)
        elif operation.startswith("Delete"):
            key = int(operation.split()[1])
            tree.delete(key)
            tree.print_tree(tree.root)
        elif operation.startswith("Search"):
            key = int(operation.split()[1])
            found = tree.search(key)
            print("True" if found else "False")
        elif operation == "Max":
            print(tree.maximum(tree.root)[1])
        elif operation == "Min":
            print(tree.minimum(tree.root)[1])
        elif operation == "Quit":
            break
