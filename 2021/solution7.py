#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print("Usage: {} <input file>".format(sys.argv[0]))
    sys.exit(1)

file_input = open(sys.argv[1], "r").read().strip().split("\n")
positions = [int(x) for x in file_input[0].split(",")]
positions.sort()
meetup = sum(positions) // len(positions) + 1

total = 0
for position in positions:
    total += sum([i for i in range(1, abs(meetup - position)+1)])
print("Total Fuel Cost: " + str(total))

