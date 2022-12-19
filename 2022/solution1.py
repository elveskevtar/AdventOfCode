#!/usr/bin/env python3
import sys
import heapq

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

def most_calories(data):
    max_calories = 0
    current_calories = 0
    for i in data:
        if i == "":
            max_calories = max(max_calories, current_calories)
            current_calories = 0
            continue
        current_calories += int(i)
    return max(max_calories, current_calories)

def top_three_sum(data):
    heap = []
    current_calories = 0
    for i in data:
        if i == "":
            heapq.heappush(heap, current_calories)
            current_calories = 0
            continue
        current_calories += int(i)
    return sum(heapq.nlargest(3, heap))

data = open(sys.argv[1], "r").read().strip().split("\n")
print(f"Top Three Sum calories: {top_three_sum(data)}")
