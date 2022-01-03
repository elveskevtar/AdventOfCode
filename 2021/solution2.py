#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

position, depth, aim = 0, 0, 0
for instruction in file_input:
    instruction_type, instruction_val = instruction.split()
    instruction_val = int(instruction_val)
    if instruction_type == "forward":
        position += instruction_val
        depth += instruction_val * aim
    elif instruction_type == "up":
        aim -= instruction_val
    elif instruction_type == "down":
        aim += instruction_val

print("Final position * depth = " + str(position * depth))

