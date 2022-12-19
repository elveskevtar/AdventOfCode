#!/usr/bin/env python3
from collections import deque
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

def add_coords(coord1, coord2):
    return (coord1[0] + coord2[0], coord1[1] + coord2[1])

def create_map(input):
    height_map = {}
    start_point = end_point = None
    for y, line in enumerate(input):
        for x, char in enumerate(line):
            height = char
            if height == "S":
                height = "a"
                start_point = (x, y)
            elif height == "E":
                height = "z"
                end_point = (x, y)
            height_map[x, y] = ord(height)
    return height_map, start_point, end_point

def shortest_path(height_map, start_point, end_point):
    steps = 0
    visited_points = {}
    next_moves = deque([(start_point, steps)])
    while len(next_moves) > 0:
        next_point, steps = next_moves.pop()
        if next_point == end_point:
            visited_points[end_point] = min(visited_points.get(next_point, steps), steps)
            continue
        if next_point in visited_points and steps >= visited_points[next_point]:
            continue
        visited_points[next_point] = min(visited_points.get(next_point, steps), steps)
        delta_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        delta_moves = [add_coords(next_point, delta) for delta in delta_moves]
        for delta_move in delta_moves:
            if delta_move not in height_map:
                continue
            if height_map[delta_move] - height_map[next_point] <= 1:
                next_steps = steps + 1
                if height_map[delta_move] == ord("a"):
                    next_steps = 0
                next_moves.append((delta_move, next_steps))
    return visited_points[end_point]

data = open(sys.argv[1], "r").read().strip().split("\n")
height_map, start_point, end_point = create_map(data)
min_steps = shortest_path(height_map, start_point, end_point)
print(f"Minimum steps to good signal: {min_steps}")
