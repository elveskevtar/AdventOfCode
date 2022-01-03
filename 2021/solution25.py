#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

field = {}
herds = [">", "v"]
for y, line in enumerate(file_input):
    if line == "":
        break
    for x, char in enumerate(line):
        if char == ".":
            continue
        field[x,y] = char

width, height = len(file_input[0]), len(file_input)
def print_field(field):
    for y in range(height):
        result = ""
        for x in range(width):
            if (x,y) not in field:
                result += "."
            else:
                result += field[x,y]
        print(result)
    print("")

num_steps, moves = 0, -1
while moves != 0:
    moves = 0
    for herd in herds:
        field_copy = dict(field)
        for pos, val in field_copy.items():
            if val == herd:
                x, y = 0, 0
                if herd == ">":
                    x = 1
                if herd == "v":
                    y = 1
                next_pos = (pos[0] + x) % width, (pos[1] + y) % height
                if next_pos in field_copy:
                    continue
                moves += 1
                field[next_pos] = herd
                field.pop(pos)
    num_steps += 1
    #print_field(field)

print("Number of steps: {}".format(num_steps))

