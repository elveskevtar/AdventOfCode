#!/usr/bin/env python3
from collections import deque
import sys

if len(sys.argv) != 3:
    print("Usage: {} <input file> <num steps>".format(sys.argv[0]))
    sys.exit(1)

steps = int(sys.argv[2])
file_input = open(sys.argv[1], "r").read().strip().split("\n")

energy_map = {}
for y, line in enumerate(file_input):
    for x, energy_level in enumerate(line):
        energy_map[x,y] = int(energy_level)

def printmap(emap, x, y):
    for j in range(y):
        result = ""
        for i in range(x):
            result += str(emap[i,j])
        print(result)
    print("")

total_flashes = 0
visited = set()
pending_flash = deque()
for i in range(steps):
    # increment all energy by 1
    pending_flash.clear()
    for (x,y), energy in energy_map.items():
        energy_map[x,y] += 1
        if energy_map[x,y] == 10:
            pending_flash.append((x,y))

    # update all flashes + all adjacents
    visited.clear()
    while len(pending_flash) != 0:
        x, y = pending_flash.popleft()
        if (x, y) in visited:
            continue
        visited.add((x,y))
        energy_map[x,y] = 0
        total_flashes += 1
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                check = (x+dx, y+dy)
                if check in energy_map.keys() and check not in visited:
                    energy_map[check] = min(10, energy_map[check] + 1)
                    if energy_map[check] == 10:
                        pending_flash.append(check)

    if len(visited) == len(file_input) * len(file_input[0]):
        print("Steps to Synchronization: {}".format(i+1))
        break

print("Final State: ")
printmap(energy_map, len(file_input), len(file_input[0]))
print("Total Flashes ({} steps): {}".format(steps, total_flashes))

