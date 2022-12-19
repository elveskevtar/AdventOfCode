#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

def is_total_overlap(left, right):
    left_start, left_end = [int(x) for x in left.split("-")]
    right_start, right_end = [int(x) for x in right.split("-")]
    return (
        (left_start <= right_start and left_end >= right_end) or
        (left_start >= right_start and left_end <= right_end)
    )

def any_overlap(left, right):
    left_start, left_end = [int(x) for x in left.split("-")]
    right_start, right_end = [int(x) for x in right.split("-")]
    return (
        (left_start >= right_start and left_start <= right_end) or
        (left_end >= right_start and left_end <= right_end) or
        is_total_overlap(left, right)
    )

data = open(sys.argv[1], "r").read().strip().split("\n")
num_total_overlaps, num_any_overlap = 0, 0
for pair in data:
    left, right = pair.split(",")
    num_total_overlaps += int(is_total_overlap(left, right))
    num_any_overlap += int(any_overlap(left, right))

print(f"Number of total overlaps: {num_total_overlaps}")
print(f"Number of any overlaps: {num_any_overlap}")
