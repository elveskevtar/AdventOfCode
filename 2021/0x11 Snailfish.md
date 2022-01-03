## --- Day 18: Snailfish ---

You descend into the ocean trench and encounter some [snailfish](https://en.wikipedia.org/wiki/Snailfish). They say they saw the sleigh keys! They'll even tell you which direction the keys went if you help one of the smaller snailfish with his _math homework_.

Snailfish numbers aren't like regular numbers. Instead, every snailfish number is a _pair_ - an ordered list of two elements. Each element of the pair can be either a regular number or another pair.

Pairs are written as `[x,y]`, where `x` and `y` are the elements within the pair. Here are some example snailfish numbers, one snailfish number per line:

```
[1,2]
[[1,2],3]
[9,[8,7]]
[[1,9],[8,5]]
[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]
```

This snailfish homework is about _addition_. To add two snailfish numbers, form a pair from the left and right parameters of the addition operator. For example, `[1,2]` + `[[3,4],5]` becomes `[[1,2],[[3,4],5]]`.

There's only one problem: _snailfish numbers must always be reduced_, and the process of adding two snailfish numbers can result in snailfish numbers that need to be reduced.

To _reduce a snailfish number_, you must repeatedly do the first action in this list that applies to the snailfish number:

-   If any pair is _nested inside four pairs_, the leftmost such pair _explodes_.
-   If any regular number is _10 or greater_, the leftmost such regular number _splits_.

Once no action in the above list applies, the snailfish number is reduced.

During reduction, at most one action applies, after which the process returns to the top of the list of actions. For example, if _split_ produces a pair that meets the _explode_ criteria, that pair _explodes_ before other _splits_ occur.

To _explode_ a pair, the pair's left value is added to the first regular number to the left of the exploding pair (if any), and the pair's right value is added to the first regular number to the right of the exploding pair (if any). Exploding pairs will always consist of two regular numbers. Then, the entire exploding pair is replaced with the regular number `0`.

Here are some examples of a single explode action:

-   `[[[[_[9,8]_,1],2],3],4]` becomes `[[[[_0_,_9_],2],3],4]` (the `9` has no regular number to its left, so it is not added to any regular number).
-   `[7,[6,[5,[4,_[3,2]_]]]]` becomes `[7,[6,[5,[_7_,_0_]]]]` (the `2` has no regular number to its right, and so it is not added to any regular number).
-   `[[6,[5,[4,_[3,2]_]]],1]` becomes `[[6,[5,[_7_,_0_]]],_3_]`.
-   `[[3,[2,[1,_[7,3]_]]],[6,[5,[4,[3,2]]]]]` becomes `[[3,[2,[_8_,_0_]]],[_9_,[5,[4,[3,2]]]]]` (the pair `[3,2]` is unaffected because the pair `[7,3]` is further to the left; `[3,2]` would explode on the next action).
-   `[[3,[2,[8,0]]],[9,[5,[4,_[3,2]_]]]]` becomes `[[3,[2,[8,0]]],[9,[5,[_7_,_0_]]]]`.

To _split_ a regular number, replace it with a pair; the left element of the pair should be the regular number divided by two and rounded _down_, while the right element of the pair should be the regular number divided by two and rounded _up_. For example, `10` becomes `[5,5]`, `11` becomes `[5,6]`, `12` becomes `[6,6]`, and so on.

Here is the process of finding the reduced result of `[[[[4,3],4],4],[7,[[8,4],9]]]` + `[1,1]`:

```
after addition: [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
after explode:  [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
after explode:  [[[[0,7],4],[15,[0,13]]],[1,1]]
after split:    [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
after split:    [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
after explode:  [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
```

Once no reduce actions apply, the snailfish number that remains is the actual result of the addition operation: `[[[[0,7],4],[[7,8],[6,0]]],[8,1]]`.

The homework assignment involves adding up a _list of snailfish numbers_ (your puzzle input). The snailfish numbers are each listed on a separate line. Add the first snailfish number and the second, then add that result and the third, then add that result and the fourth, and so on until all numbers in the list have been used once.

For example, the final sum of this list is `[[[[1,1],[2,2]],[3,3]],[4,4]]`:

```
[1,1]
[2,2]
[3,3]
[4,4]
```

The final sum of this list is `[[[[3,0],[5,3]],[4,4]],[5,5]]`:

```
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
```

The final sum of this list is `[[[[5,0],[7,4]],[5,5]],[6,6]]`:

```
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]
```

Here's a slightly larger example:

```
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
```

The final sum `[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]` is found after adding up the above snailfish numbers:

```
  [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
+ [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
= [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]

  [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
+ [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
= [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]

  [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]
+ [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
= [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]

  [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]
+ [7,[5,[[3,8],[1,4]]]]
= [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]

  [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]
+ [[2,[2,2]],[8,[8,1]]]
= [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]

  [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]
+ [2,9]
= [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]

  [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]
+ [1,[[[9,3],9],[[9,0],[0,7]]]]
= [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]

  [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]
+ [[[5,[7,4]],7],1]
= [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]

  [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]
+ [[[[4,2],2],6],[8,7]]
= [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]
```

To check whether it's the right answer, the snailfish teacher only checks the _magnitude_ of the final sum. The magnitude of a pair is 3 times the magnitude of its left element plus 2 times the magnitude of its right element. The magnitude of a regular number is just that number.

For example, the magnitude of `[9,1]` is `3*9 + 2*1 = _29_`; the magnitude of `[1,9]` is `3*1 + 2*9 = _21_`. Magnitude calculations are recursive: the magnitude of `[[9,1],[1,9]]` is `3*29 + 2*21 = _129_`.

Here are a few more magnitude examples:

-   `[[1,2],[[3,4],5]]` becomes `_143_`.
-   `[[[[0,7],4],[[7,8],[6,0]]],[8,1]]` becomes `_1384_`.
-   `[[[[1,1],[2,2]],[3,3]],[4,4]]` becomes `_445_`.
-   `[[[[3,0],[5,3]],[4,4]],[5,5]]` becomes `_791_`.
-   `[[[[5,0],[7,4]],[5,5]],[6,6]]` becomes `_1137_`.
-   `[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]` becomes `_3488_`.

So, given this example homework assignment:

```
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
```

The final sum is:

```
[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
```

The magnitude of this final sum is `_4140_`.

Add up all of the snailfish numbers from the homework assignment in the order they appear. _What is the magnitude of the final sum?_

```python
#!/usr/bin/env python3
from collections import deque
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

while len(trees) > 1:
    tree1 = trees.pop()
    tree2 = trees.pop()
    new_node = SnailfishNode(left=tree1, right=tree2)
    tree1.parent = new_node
    tree2.parent = new_node
    new_node.reduce()
    trees.append(new_node)

print("Final Magnitude: {}".format(trees[0].magnitude()))
```

```bash
❯ python3 solution18.py input18
Final Magnitude: 3763
```

## --- Part Two ---

You notice a second question on the back of the homework assignment:

What is the largest magnitude you can get from adding only two of the snailfish numbers?

Note that snailfish addition is not [commutative](https://en.wikipedia.org/wiki/Commutative_property) - that is, `x + y` and `y + x` can produce different results.

Again considering the last example homework assignment above:

```
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
```

The largest magnitude of the sum of any two snailfish numbers in this list is `_3993_`. This is the magnitude of `[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]` + `[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]`, which reduces to `[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]]`.

_What is the largest magnitude of any sum of two different snailfish numbers from the homework assignment?_

New last section:
```python
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
```

```bash
❯ python3 solution18.py input18
Maximum Magnitude: 4664
```