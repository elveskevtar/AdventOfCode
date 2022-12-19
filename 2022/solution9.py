#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

def add_coords(coord1, coord2):
    return (coord1[0] + coord2[0], coord1[1] + coord2[1])

def is_touching(coord1, coord2):
    return abs(coord1[0] - coord2[0]) <= 1 and abs(coord1[1] - coord2[1]) <= 1

def new_tail_location(head_location, tail_location):
    delta_x = head_location[0] - tail_location[0]
    if delta_x != 0:
        delta_x = delta_x // abs(delta_x)
    delta_y = head_location[1] - tail_location[1]
    if delta_y != 0:
        delta_y = delta_y // abs(delta_y)
    return add_coords(tail_location, (delta_x, delta_y))

def get_delta(direction):
    if direction == "L":
        return (-1, 0)
    if direction == "R":
        return (1, 0)
    if direction == "U":
        return (0, -1)
    if direction == "D":
        return (0, 1)
    # should never reach here
    print(f"ERROR: invalid direction {direction}")
    sys.exit(1)

def simulate_motion(movements):
    knots = [(0, 0) for _ in range(10)]  # head is start of the list, tail is end
    tail_visited = {knots[-1]}
    for movement in movements:
        direction, spaces = movement.split()
        spaces = int(spaces)
        delta_move = get_delta(direction)
        for _ in range(spaces):
            knots[0] = add_coords(knots[0], delta_move)
            for i in range(9):
                if not is_touching(knots[i], knots[i + 1]):
                    knots[i + 1] = new_tail_location(knots[i], knots[i + 1])
                else:
                    break
            tail_visited.add(knots[-1])
    print(f"{len(tail_visited)} unique tail locations")

data = open(sys.argv[1], "r").read().strip().split("\n")
simulate_motion(data)
