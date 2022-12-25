#!/usr/bin/env python3
import os
import sys
import time

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

def add_coords(coord1, coord2):
    return (coord1[0] + coord2[0], coord1[1] + coord2[1])

def print_map(rock_map, xmin, xmax, ymin, ymax):
    print("\033c")
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            if (x, y) not in rock_map:
                print(" ", end="")
            else:
                print(rock_map[x, y], end="")
        print("")

def create_map(data):
    rock_map, ymax = {(500, 0): "+"}, 0
    for structure in data:
        points = structure.split(" -> ")
        for i in range(len(points) - 1):
            x1, y1 = [int(i) for i in points[i].split(",")]
            x2, y2 = [int(i) for i in points[i+1].split(",")]
            if x1 - x2 != 0:
                y = y1
                ymax = max(y, ymax)
                xdiff = (x2 - x1) // abs(x2 - x1)
                for x in range(x1, x2 + xdiff, xdiff):
                    rock_map[x, y] = "#"
            elif y1 - y2 != 0:
                x = x1
                ydiff = (y2 - y1) // abs(y2 - y1)
                for y in range(y1, y2 + ydiff, ydiff):
                    ymax = max(y, ymax)
                    rock_map[x, y] = "#"
    return rock_map, ymax

def simulate_sand(rock_map: dict, ymax):
    terminal_size = os.get_terminal_size()
    rows = terminal_size.lines - 1
    cols = terminal_size.columns
    sand_units, next_sand = 1, (500, 0)
    while True:
        rock_map[next_sand] = "o"
        # time.sleep(0.05)
        # print_map(
        #     rock_map, next_sand[0] - (cols // 2), next_sand[0] + (cols // 2),
        #     next_sand[1] - (rows // 2), next_sand[1] + (rows // 2) + 1
        # )
        if next_sand[1] < ymax + 1:
            if add_coords(next_sand, (0, 1)) not in rock_map:
                rock_map.pop(next_sand)
                next_sand = add_coords(next_sand, (0, 1))
            elif add_coords(next_sand, (-1, 1)) not in rock_map:
                rock_map.pop(next_sand)
                next_sand = add_coords(next_sand, (-1, 1))
            elif add_coords(next_sand, (1, 1)) not in rock_map:
                rock_map.pop(next_sand)
                next_sand = add_coords(next_sand, (1, 1))
            elif next_sand == (500, 0):
                break
            else:
                sand_units += 1
                next_sand = (500, 0)
        else:
            sand_units += 1
            next_sand = (500, 0)
    return sand_units

data = open(sys.argv[1], "r").read().strip().split("\n")
rock_map, ymax = create_map(data)
print(f"Sand units: {simulate_sand(rock_map, ymax)}")
