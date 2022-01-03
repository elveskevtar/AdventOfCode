#!/usr/bin/env python3
from collections import defaultdict, deque
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

connections = defaultdict(list)
for line in file_input:
    first, second = line.split("-")
    connections[first].append(second)
    connections[second].append(first)

def valid_path(check, move):
    if move == "start":
        return False
    double_small = None
    frequencies = {name:check.count("{}".format(name)) for name in check.split(",")}
    for name, frequency in frequencies.items():
        if frequency == 2 and name.islower():
            double_small = name
    if double_small is not None and (double_small == move or move in frequencies):
        return False
    return True

paths = set()
queue = deque()
queue.append("start")
while len(queue) != 0:
    check = queue.popleft()
    last_node = check.split(",")[-1]
    if last_node == "end":
        paths.add(check)
        continue
    for move in connections[last_node]:
        if valid_path(check, move) or move.isupper():
            queue.append("{},{}".format(check, move))

print("Total Unique Paths: {}".format(len(paths)))

