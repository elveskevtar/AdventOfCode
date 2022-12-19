#!/usr/bin/env python3
from collections import deque
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

def get_rearrangement(instructions):
    num_stacks = 9
    stacks = [deque() for _ in range(num_stacks)]
    for instruction in instructions[:8]:
        for stack in range(num_stacks):
            label = instruction[stack * 4 + 1]
            if label != " ":
                stacks[stack].appendleft(label)
    
    for instruction in instructions[10:-1]:
        num_moves = int(instruction.split()[1])
        start = int(instruction.split()[3]) - 1
        dest = int(instruction.split()[5]) - 1
        stacks[dest].extend(
            reversed([stacks[start].pop() for _ in range(num_moves)])
        )

    return "".join([stack.pop() for stack in stacks])

data = open(sys.argv[1], "r").read().split("\n")
print(f"Top of stacks labels: {get_rearrangement(data)}")
