#!/usr/bin/env python3
from collections import deque
from copy import deepcopy
from math import floor, ceil
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

class SnailfishNode:
    def __init__(self, val=None, left=None, right=None, parent=None):
        """
        Invariants:
        1. Each node has either a data value or has left and right, never both
        2. A pair node (no value) should have both left and right != None
        3. A value node (value != None) should always have a parent (always in pair)
        """
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent

    def depth(self):
        node, depth = self, 1
        while node.parent:
            node = node.parent
            depth += 1
        return depth

    def find_left(self):
        node = self.parent
        if self == node.left:
            while node.parent and node == node.parent.left:
                node = node.parent
            if not node.parent:
                return None
            node = node.parent

        node = node.left
        while node.val is None:
            node = node.right
        return node

    def find_right(self):
        node = self.parent
        if self == node.right:
            while node.parent and node == node.parent.right:
                node = node.parent
            if not node.parent:
                return None
            node = node.parent

        node = node.right
        while node.val is None:
            node = node.left
        return node

    def explode(self):
        """
        Preconditions:
        1. Node is a pair node
        2. Node points to two value nodes
        3. Occurs if only if depth > 4
        """
        left = self.find_left()
        right = self.find_right()
        if left:
            left.val += self.left.val
        if right:
            right.val += self.right.val
        self.left = None
        self.right = None
        self.val = 0

    def split(self):
        """
        Preconditions:
        1. Node is a value node
        2. Occurs only if value is >= 10
        """
        left_val = floor(self.val / 2)
        right_val = ceil(self.val / 2)
        left_node = SnailfishNode(val=left_val, parent=self)
        right_node = SnailfishNode(val=right_val, parent=self)
        self.val, self.left, self.right = None, left_node, right_node

    def reduce(self):
        """
        Fully reduces tree by exploding heavily nested pairs and splitting large nums
        """
        stack = deque()
        while True:
            exploded, splitted = False, False
            stack.clear()
            stack.append(self)
            while len(stack) != 0:
                node = stack.pop()
                if node.val is not None:
                    continue
                stack.append(node.right)
                stack.append(node.left)
                if node.left.val is not None and node.right.val is not None \
                        and node.depth() > 4:
                    node.explode()
                    exploded = True
                    break
            if exploded:
                continue
            
            stack.clear()
            stack.append(self)
            while len(stack) != 0:
                node = stack.pop()
                if node.val is None:
                    stack.append(node.right)
                    stack.append(node.left)
                    continue
                if node.val >= 10:
                    node.split()
                    splitted = True
                    break
            if not splitted:
                break

    def magnitude(self):
        """
        Calculate the magnitude of the entire tree
        """
        if self.val is not None:
            return self.val
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()


trees = deque()
for line in file_input[::-1]:
    if line == "":
        continue
    line = line[1:-1]
    root = curr = SnailfishNode()
    for char in line:
        if char == "[":
            node = SnailfishNode(parent=curr)
            if not curr.left:
                curr.left = node
            else:
                curr.right = node
            curr = node
        elif char.isnumeric():
            node = SnailfishNode(val=int(char), parent=curr)
            if not curr.left:
                curr.left = node
            else:
                curr.right = node
        elif char == "]":
            curr = curr.parent
    trees.append(root)

max_magnitude = 0
for _tree1 in trees:
    for _tree2 in trees:
        if _tree1 == _tree2:
            continue
        tree1 = deepcopy(_tree1)
        tree2 = deepcopy(_tree2)
        new_node = SnailfishNode(left=tree1, right=tree2)
        tree1.parent = new_node
        tree2.parent = new_node
        new_node.reduce()
        max_magnitude = max(max_magnitude, new_node.magnitude())

print("Maximum Magnitude: {}".format(max_magnitude))

#while len(trees) > 1:
#    tree1 = trees.pop()
#    tree2 = trees.pop()
#    new_node = SnailfishNode(left=tree1, right=tree2)
#    tree1.parent = new_node
#    tree2.parent = new_node
#    new_node.reduce()
#    trees.append(new_node)
#
#print("Final Magnitude: {}".format(trees[0].magnitude()))

