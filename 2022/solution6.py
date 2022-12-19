#!/usr/bin/env python3
from collections import deque
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file>")
    sys.exit(1)

def get_marker_end(signal, num_unique):
    marker = deque(signal[:num_unique-1])
    for idx, char in enumerate(signal[num_unique-1:]):
        marker.append(char)
        if len(set(marker)) == num_unique:
            return idx + num_unique
        marker.popleft()
    return idx

data = open(sys.argv[1], "r").read().rstrip()
print(f"Marker end: {get_marker_end(data, 14)}")
