#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

field = {}
file_input = open(sys.argv[1], "r").read().strip().split("\n")

def delta(p1, p2):
    if p1 > p2:
        return -1
    return int(p1 != p2)

for line in file_input:
    start, end = line.split(" -> ")
    x1, y1 = list(map(lambda x: int(x), start.split(",")))
    x2, y2 = list(map(lambda x: int(x), end.split(",")))
    delta_x, delta_y = delta(x1, x2), delta(y1, y2)
    x, y = x1, y1
    while x != x2 or y != y2:
        field[x,y] = field.get((x,y),0) + 1
        x += delta_x
        y += delta_y
    field[x,y] = field.get((x,y),0) + 1

num_points = sum(list(map(lambda x: x >= 2, field.values())))
print("Dangerous Points: " + str(num_points))

