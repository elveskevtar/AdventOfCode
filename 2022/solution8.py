#!/usr/bin/env python3
import sys
from typing import List, Set

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

def generate_map(data):
    tree_map = []
    for line in data:
        tree_map.append([int(num) for num in line])
    return tree_map

def find_visible_trees(
    treeline: List, visible_trees: Set, reversed=False, x=None, y=None
):
    def coord(i):
        j = len(treeline) - 1 - i if reversed else i
        if x is not None:
            return (x, j)
        return (j, y)

    curr_height = 0
    for i, height in enumerate(treeline):
        last_height = curr_height
        curr_height = max(curr_height, height)
        if coord(i) in visible_trees:
            continue
        if i == 0 or height > last_height:
            visible_trees.add(coord(i))

def calculate_num_visible(tree_map):
    visible_trees = set()
    for y, horizontal in enumerate(tree_map):
        find_visible_trees(horizontal, visible_trees, y=y)
        find_visible_trees(list(reversed(horizontal)), visible_trees, reversed=True, y=y)
    for x in range(len(tree_map[0])):
        vertical = [horizontal[x] for horizontal in tree_map]
        find_visible_trees(vertical, visible_trees, x=x)
        find_visible_trees(list(reversed(vertical)), visible_trees, reversed=True, x=x)

    return len(visible_trees)

def highest_scenic_view(tree_map):
    max_scenic_view = 0
    width, length = len(tree_map[0]), len(tree_map)
    for y, horizontal in enumerate(tree_map):
        for x, height in enumerate(horizontal):
            left, right, up, down = 0, 0, 0, 0
            nx = x - 1
            while nx >= 0:
                left += 1
                if tree_map[y][nx] >= height:
                    break
                nx -= 1
            nx = x + 1
            while nx < width:
                right += 1
                if tree_map[y][nx] >= height:
                    break
                nx += 1
            ny = y - 1
            while ny >= 0:
                up += 1
                if tree_map[ny][x] >= height:
                    break
                ny -= 1
            ny = y + 1
            while ny < length:
                down += 1
                if tree_map[ny][x] >= height:
                    break
                ny += 1
            max_scenic_view = max(max_scenic_view, left * right * up * down)
    return max_scenic_view

data = open(sys.argv[1], "r").read().strip().split("\n")
tree_map = generate_map(data)
print(f"Number of tree visible:\t{calculate_num_visible(tree_map)}")
print(f"Max scenic view:\t{highest_scenic_view(tree_map)}")
