#!/usr/bin/env python3
from collections import deque
from functools import reduce
import heapq
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

heightmap = {}
for y, line in enumerate(file_input):
    for x, val in enumerate(line):
        heightmap[x,y] = int(val)

total = 0
for (x, y), val in heightmap.items():
    low = True
    for dx in [-1,1]:
        if (x + dx, y) in heightmap and heightmap[x+dx,y] <= val:
            low = False
    for dy in [-1,1]:
        if (x, y + dy) in heightmap and heightmap[x,y+dy] <= val:
            low = False
    if low:
        total += 1 + val

basin_queue = deque()
visited = set()
largest_basins = []
for (x, y), val in heightmap.items():
    if val == 9 or (x, y) in visited:
        continue
    basin_queue.clear()
    basin_queue.append((x,y))
    basin_length = 0
    while len(basin_queue) != 0:
        x1, y1 = basin_queue.pop()
        if (x1, y1) in visited:
            continue
        basin_length += 1
        visited.add((x1,y1))
        for dx in [-1,1]:
            check = (x1 + dx, y1)
            if check in heightmap and heightmap[check] != 9:
                basin_queue.append(check)
        for dy in [-1,1]:
            check = (x1, y1 + dy)
            if check in heightmap and heightmap[check] != 9:
                basin_queue.append(check)
    heapq.heappush(largest_basins, basin_length)

largest = reduce(lambda x, y: x * y, heapq.nlargest(3, largest_basins))
print("Risk Level: " + str(total))
print("Largest Basins: " + str(largest))

