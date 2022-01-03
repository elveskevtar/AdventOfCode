#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")

freq_map = {}
for start in file_input[0].split(","):
    start = int(start)
    freq_map[start] = freq_map.get(start, 0) + 1

days = 80
for x in range(days):
    for start, frequency in dict(freq_map).items():
        freq_map[start] -= frequency
        if start == 0:
            freq_map[8] = freq_map.get(8, 0) + frequency
            freq_map[6] = freq_map.get(6, 0) + frequency
        else:
            freq_map[start-1] = freq_map.get(start-1, 0) + frequency

print("Total Lanternfish ({} days): {}".format(days, sum(freq_map.values())))

