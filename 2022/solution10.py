#!/usr/bin/env python3
from collections import deque
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

crt_pixels = []

def print_image():
    for i, pixel in enumerate(crt_pixels):
        print(pixel, end="")
        if (i + 1) % 40 == 0:
            print("\n", end="")

def handle_cycle(cycle, register_x):
    pixel = "." if abs(register_x - ((cycle - 1) % 40)) > 1 else "#"
    crt_pixels.append(pixel)
    if (cycle - 20) % 40 == 0:
        return cycle * register_x
    return 0

def process_instructions(instructions):
    cycle = 1
    register_x = 1
    signal_strengths = 0
    for instruction in instructions:
        if instruction == "noop":
            cycle += 1
            signal_strengths += handle_cycle(cycle, register_x)
            continue
        
        cycle += 1
        signal_strengths += handle_cycle(cycle, register_x)
        cycle += 1
        register_x += int(instruction.split()[1])
        signal_strengths += handle_cycle(cycle, register_x)

    return signal_strengths

data = open(sys.argv[1], "r").read().strip().split("\n")
process_instructions(data)
print_image()
