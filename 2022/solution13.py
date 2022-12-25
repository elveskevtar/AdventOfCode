#!/usr/bin/env python3
from collections import deque
import functools
import sys

def compare(left, right, root=True):
    if isinstance(left, int) and isinstance(right, int):
        if left > right:
            return -1
        if left < right:
            return 1
        return 0
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    left, right = deque(left), deque(right)
    while len(left) > 0 and len(right) > 0:
        next_left, next_right = left.popleft(), right.popleft()
        cmp = compare(next_left, next_right, False)
        if cmp != 0:
            return cmp
    if len(left) > 0:
        return -1
    if len(right) > 0:
        return 1
    return 1 if root else 0

def parse_pairs(data):
    pairs_sum = 0
    for idx, i in enumerate(range(0, len(data), 3)):
        left = eval(data[i])
        right = eval(data[i+1])
        cmp = compare(left, right, True)
        if cmp == 1:
            pairs_sum += idx + 1
    print(f"pairs_sum = {pairs_sum}")

def sort_pairs(data):
    packets = [[[2]], [[6]]]
    for packet in data:
        if packet == "":
            continue
        packets.append(eval(packet))
    packets.sort(key=functools.cmp_to_key(compare), reverse=True)
    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)

data = open(sys.argv[1], "r").read().strip().split("\n")
print(f"decoder key: {sort_pairs(data)}")
