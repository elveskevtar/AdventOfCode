#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

def count_increases(data: list[int], window: int = 1) -> int:
    num_increased = 0
    for i in range(len(data) - window):
        s1 = sum([int(data[i+j]) for j in range(window)])
        s2 = sum([int(data[i+j+1]) for j in range(window)])
        if s2 > s1:
            num_increased += 1
    return num_increased

data = open(sys.argv[1], "r").read().strip().split("\n")
print("# increases: " + str(count_increases(data)))
print("# 3-window increases: " + str(count_increases(data, 3)))

