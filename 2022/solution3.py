#!/usr/bin/env python3
from itertools import islice
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

LOWER_DIFF = ord("a") - 1
UPPER_DIFF = ord("A") - 27

def caculate_priority(rucksacks):
    total_priority = 0
    grouped_rucksacks = [
        rucksacks[i:i + 3] for i in range(0, len(rucksacks), 3)
    ]
    for group in grouped_rucksacks:
        badge = set.intersection(
            *[set(rucksack) for rucksack in group]
        ).pop()
        if badge.islower():
            diff = LOWER_DIFF
        else:
            diff = UPPER_DIFF
        priority = ord(badge) - diff
        total_priority += priority
    return total_priority

data = open(sys.argv[1], "r").read().strip().split("\n")
print(f"Total priority would be {caculate_priority(data)}")
