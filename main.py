class Node:
    def __init__(self, value, color="RED"):
        self.value = value
        self.color = color  # RED or BLACK
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(value=None, color="BLACK")
        self.root = self.TNULL

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

    def fix_insert(self, k):
        while k.parent.color == "RED":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left  # uncle
                if u.color == "RED":
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.left_rotate(k.parent.parent)
            else:
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
        self.root.color = "BLACK"

    def fix_delete(self, x):
        while x != self.root and x.color == "BLACK":
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
        if y is None:
            self.root = node
        elif node.value < y.value:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = "BLACK"
            return

        if node.parent.parent is None:
            return

        self.fix_insert(node)

    def delete(self, key):
        def transplant(u, v):
            if u.parent is None:
                self.root = v
            elif u == u.parent.left:
                u.parent.left = v
            else:
                u.parent.right = v
            v.parent = u.parent

        z = self.root
        while z != self.TNULL:
            if z.value == key:
                break
            elif key < z.value:
                z = z.left
            else:
                z = z.right

        if z == self.TNULL:
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            transplant(z, z.left)
        else:
            y = self.minimum(z.right)[0]
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "BLACK":
            self.fix_delete(x)

    def search(self, key):
        node = self.root
        while node != self.TNULL and key != node.value:
            if key < node.value:
                node = node.left
            else:
                node = node.right
        return node != self.TNULL

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node, node.value

    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node, node.value

    def print_tree(self, node, indent="", last=True):
        if node != self.TNULL:
            print(indent, end="")
            if last:
                print("└──", end="")
                indent += "   "
            else:
                print("├──", end="")
                indent += "│  "
            color = "R" if node.color == "RED" else "B"
            print(f"{color}{node.value}")
            self.print_tree(node.left, indent, False)
            self.print_tree(node.right, indent, True)

if __name__ == "__main__":
    tree = RedBlackTree()

    inputs = list(map(int, input("Enter space-separated values to insert: ").split()))
    for value in inputs:
        tree.insert(value)
    tree.print_tree(tree.root)

    while True:
        operation = input("Enter operation (e.g., Delete 35, Search 40, Max, Min, Quit): ")
        if operation.startswith("Delete"):
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
